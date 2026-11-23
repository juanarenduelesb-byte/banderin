-- Banderín · Social (versión de prueba): perfiles de jugador, amigos, partidas, solicitudes, bloqueos y denuncias.
-- Ejecutar UNA vez en Supabase → SQL Editor. Usa las mismas cuentas de Banderín (auth.users).
-- Todo está protegido por seguridad por filas (RLS): nadie lee ni toca lo que no le corresponde.
-- Para quitarlo entero: ver el bloque «DESHACER» al final.

-- ───────────────────────── Edad (privada) ─────────────────────────
-- La fecha de nacimiento solo la ve su dueño. Mínimo 16 años. No se puede cambiar una vez puesta.
create table if not exists public.social_privado (
  user_id    uuid primary key references auth.users (id) on delete cascade,
  nacimiento date not null,
  aceptado   timestamptz not null default now()  -- cuándo aceptó las normas de Social y la política de privacidad
);
alter table public.social_privado add column if not exists aceptado timestamptz not null default now();
create or replace function public.social_edad_ok() returns trigger language plpgsql as $$
begin
  if new.user_id <> auth.uid() then raise exception 'no permitido'; end if;
  new.aceptado := now();
  if new.nacimiento > (current_date - interval '16 years')::date or new.nacimiento < date '1910-01-01' then
    raise exception 'edad: hay que tener al menos 16 años';
  end if;
  return new;
end $$;
drop trigger if exists social_edad on public.social_privado;
create trigger social_edad before insert on public.social_privado for each row execute function public.social_edad_ok();

-- ───────────────────────── Perfil de jugador ─────────────────────────
create table if not exists public.social_perfiles (
  user_id    uuid primary key references auth.users (id) on delete cascade,
  nombre     text not null check (char_length(btrim(nombre)) between 2 and 40),
  hcp        numeric(3,1) check (hcp between -10 and 54),
  provincia  text check (char_length(provincia) <= 40),
  campos     text[] not null default '{}' check (cardinality(campos) <= 8),
  bio        text check (char_length(bio) <= 280),
  visible    boolean not null default true,   -- aparece en «Jugadores»
  mayor      boolean not null default false,  -- lo calcula el servidor; nadie más lo ve
  creado     timestamptz not null default now(),
  actualizado timestamptz not null default now()
);

-- ───────────────────────── Contacto (se ve solo si toca) ─────────────────────────
create table if not exists public.social_contacto (
  user_id  uuid primary key references auth.users (id) on delete cascade,
  whatsapp text check (whatsapp ~ '^\+?[0-9 ]{9,17}$'),
  email    text check (char_length(email) <= 120 and email ~* '^[^@\s]+@[^@\s]+\.[^@\s]+$'),
  publico  boolean not null default false     -- solo mayores de 18 pueden hacerlo público
);

-- ───────────────────────── Amigos ─────────────────────────
create table if not exists public.social_amistades (
  de     uuid not null references auth.users (id) on delete cascade,
  para   uuid not null references auth.users (id) on delete cascade,
  estado text not null default 'pendiente' check (estado in ('pendiente', 'aceptada')),
  creado timestamptz not null default now(),
  primary key (de, para),
  check (de <> para)
);
create index if not exists social_amistades_para on public.social_amistades (para);

-- ───────────────────────── Partidas ─────────────────────────
create table if not exists public.social_partidas (
  id          uuid primary key default gen_random_uuid(),
  autor       uuid not null default auth.uid() references auth.users (id) on delete cascade,
  campo       text not null check (char_length(campo) between 2 and 80),
  provincia   text check (char_length(provincia) <= 40),
  fecha       date not null,
  hora        time,
  tipo        text not null default 'partida' check (tipo in ('partida', 'torneo')),
  torneo      text check (char_length(torneo) <= 160),
  torneo_url  text check (char_length(torneo_url) <= 300 and torneo_url like 'https://%'),
  plazas      smallint not null default 1 check (plazas between 1 and 3),
  hcp_min     numeric(3,1) check (hcp_min between -10 and 54),
  hcp_max     numeric(3,1) check (hcp_max between -10 and 54),
  nota        text check (char_length(nota) <= 280),
  solo_amigos boolean not null default false,
  cerrada     boolean not null default false,
  creado      timestamptz not null default now()
);
create index if not exists social_partidas_fecha on public.social_partidas (fecha);
create index if not exists social_partidas_autor on public.social_partidas (autor);

-- ───────────────────────── Solicitudes para unirse ─────────────────────────
create table if not exists public.social_solicitudes (
  partida uuid not null references public.social_partidas (id) on delete cascade,
  jugador uuid not null references auth.users (id) on delete cascade,
  mensaje text check (char_length(mensaje) <= 200),
  estado  text not null default 'pendiente' check (estado in ('pendiente', 'aceptada', 'rechazada')),
  creado  timestamptz not null default now(),
  primary key (partida, jugador)
);
create index if not exists social_solicitudes_jugador on public.social_solicitudes (jugador);

-- ───────────────────────── Bloqueos y denuncias ─────────────────────────
create table if not exists public.social_bloqueos (
  quien  uuid not null references auth.users (id) on delete cascade,
  a_quien uuid not null references auth.users (id) on delete cascade,
  creado timestamptz not null default now(),
  primary key (quien, a_quien),
  check (quien <> a_quien)
);
create table if not exists public.social_denuncias (
  id      bigint generated always as identity primary key,
  quien   uuid not null default auth.uid() references auth.users (id) on delete cascade,
  contra  uuid references auth.users (id) on delete set null,
  partida uuid references public.social_partidas (id) on delete set null,
  motivo  text not null check (motivo in ('acoso', 'spam', 'suplantacion', 'contenido', 'menor', 'otro')),
  texto   text check (char_length(texto) <= 500),
  creado  timestamptz not null default now(),
  revisada boolean not null default false
);

-- ───────────────────────── Funciones de ayuda (no exponen datos) ─────────────────────────
create or replace function public.social_bloqueo(a uuid, b uuid) returns boolean
language sql stable security definer set search_path = public as $$
  select exists (select 1 from social_bloqueos where (quien = a and a_quien = b) or (quien = b and a_quien = a));
$$;
create or replace function public.social_amigos(a uuid, b uuid) returns boolean
language sql stable security definer set search_path = public as $$
  select exists (select 1 from social_amistades where estado = 'aceptada' and ((de = a and para = b) or (de = b and para = a)));
$$;
-- Conectados: uno aceptó al otro en una partida, o los dos están aceptados en la misma.
create or replace function public.social_conectados(a uuid, b uuid) returns boolean
language sql stable security definer set search_path = public as $$
  select exists (
    select 1 from social_partidas p join social_solicitudes s on s.partida = p.id and s.estado = 'aceptada'
    where (p.autor = a and s.jugador = b) or (p.autor = b and s.jugador = a)
  ) or exists (
    select 1 from social_solicitudes s1 join social_solicitudes s2 on s1.partida = s2.partida
    where s1.estado = 'aceptada' and s2.estado = 'aceptada' and s1.jugador = a and s2.jugador = b
  );
$$;
create or replace function public.social_tiene_perfil(u uuid) returns boolean
language sql stable security definer set search_path = public as $$
  select exists (select 1 from social_perfiles where user_id = u);
$$;
create or replace function public.social_autor(pid uuid) returns uuid
language sql stable security definer set search_path = public as $$
  select autor from social_partidas where id = pid;
$$;
create or replace function public.social_ve_partida(pid uuid) returns boolean
language sql stable security definer set search_path = public as $$
  select exists (select 1 from social_partidas p where p.id = pid and not social_bloqueo(auth.uid(), p.autor)
                 and (p.autor = auth.uid() or not p.solo_amigos or social_amigos(auth.uid(), p.autor)));
$$;
-- Mi estado (lo único que el cliente sabe del campo «mayor»: el suyo).
create or replace function public.social_mi_estado() returns json
language sql stable security definer set search_path = public as $$
  select json_build_object(
    'edad', exists (select 1 from social_privado where user_id = auth.uid()),
    'mayor', coalesce((select nacimiento <= (current_date - interval '18 years')::date from social_privado where user_id = auth.uid()), false),
    'perfil', exists (select 1 from social_perfiles where user_id = auth.uid()));
$$;

-- ───────────────────────── Reglas que el cliente no puede saltarse ─────────────────────────
create or replace function public.social_perfil_guard() returns trigger language plpgsql security definer set search_path = public as $$
begin
  if new.user_id <> auth.uid() then raise exception 'no permitido'; end if;
  if not exists (select 1 from social_privado where user_id = new.user_id) then raise exception 'edad: falta la fecha de nacimiento'; end if;
  new.mayor := (select nacimiento <= (current_date - interval '18 years')::date from social_privado where user_id = new.user_id);
  new.nombre := btrim(new.nombre);
  new.actualizado := now();
  if tg_op = 'UPDATE' then new.creado := old.creado; end if;
  return new;
end $$;
drop trigger if exists social_perfil_guard on public.social_perfiles;
create trigger social_perfil_guard before insert or update on public.social_perfiles for each row execute function public.social_perfil_guard();

create or replace function public.social_contacto_guard() returns trigger language plpgsql security definer set search_path = public as $$
begin
  if new.user_id <> auth.uid() then raise exception 'no permitido'; end if;
  -- Menores de 18: su contacto nunca es público (solo amigos y jugadores aceptados).
  if new.publico and not coalesce((select nacimiento <= (current_date - interval '18 years')::date from social_privado where user_id = new.user_id), false) then
    new.publico := false;
  end if;
  return new;
end $$;
drop trigger if exists social_contacto_guard on public.social_contacto;
create trigger social_contacto_guard before insert or update on public.social_contacto for each row execute function public.social_contacto_guard();

create or replace function public.social_amistad_guard() returns trigger language plpgsql security definer set search_path = public as $$
begin
  if tg_op = 'INSERT' then
    if social_bloqueo(new.de, new.para) then raise exception 'no permitido'; end if;
    if (select count(*) from social_amistades where de = new.de and creado > now() - interval '1 day') >= 30 then raise exception 'limite'; end if;
    -- Si el otro ya me la había pedido, se acepta directamente.
    if exists (select 1 from social_amistades where de = new.para and para = new.de) then
      update social_amistades set estado = 'aceptada' where de = new.para and para = new.de;
      return null;
    end if;
    new.estado := 'pendiente';
  else
    if new.de <> old.de or new.para <> old.para then raise exception 'no permitido'; end if;
  end if;
  return new;
end $$;
drop trigger if exists social_amistad_guard on public.social_amistades;
create trigger social_amistad_guard before insert or update on public.social_amistades for each row execute function public.social_amistad_guard();

create or replace function public.social_partida_guard() returns trigger language plpgsql security definer set search_path = public as $$
begin
  if tg_op = 'INSERT' then
    new.autor := auth.uid();
    if not social_tiene_perfil(new.autor) then raise exception 'perfil: crea tu perfil primero'; end if;
    if (select count(*) from social_partidas where autor = new.autor and creado > now() - interval '1 day') >= 6 then raise exception 'limite'; end if;
    new.creado := now();
    -- Limpieza: las partidas (con sus solicitudes y su chat) se borran 30 días después de jugarse.
    delete from social_partidas where fecha < current_date - 30;
  else
    new.autor := old.autor; new.creado := old.creado;
  end if;
  if new.fecha < current_date or new.fecha > current_date + 180 then raise exception 'fecha: entre hoy y dentro de 6 meses'; end if;
  if new.hcp_min is not null and new.hcp_max is not null and new.hcp_min > new.hcp_max then raise exception 'hcp: el mínimo es mayor que el máximo'; end if;
  return new;
end $$;
drop trigger if exists social_partida_guard on public.social_partidas;
create trigger social_partida_guard before insert or update on public.social_partidas for each row execute function public.social_partida_guard();

create or replace function public.social_solicitud_guard() returns trigger language plpgsql security definer set search_path = public as $$
declare p social_partidas;
begin
  select * into p from social_partidas where id = coalesce(new.partida, old.partida);
  if tg_op = 'INSERT' then
    if new.jugador <> auth.uid() then raise exception 'no permitido'; end if;
    if not social_tiene_perfil(new.jugador) then raise exception 'perfil: crea tu perfil primero'; end if;
    if p.autor = new.jugador or p.cerrada or p.fecha < current_date or social_bloqueo(p.autor, new.jugador) then raise exception 'no permitido'; end if;
    if (select count(*) from social_solicitudes where jugador = new.jugador and creado > now() - interval '1 day') >= 30 then raise exception 'limite'; end if;
    new.estado := 'pendiente'; new.creado := now();
  else
    if new.partida <> old.partida or new.jugador <> old.jugador then raise exception 'no permitido'; end if;
    -- Solo quien publica la partida acepta o rechaza; el jugador solo puede retirar su mensaje.
    if new.estado <> old.estado and auth.uid() <> p.autor then raise exception 'no permitido'; end if;
    if new.estado = 'aceptada' and old.estado <> 'aceptada' and
       (select count(*) from social_solicitudes where partida = new.partida and estado = 'aceptada') >= p.plazas then
      raise exception 'plazas: la partida ya está completa';
    end if;
  end if;
  return new;
end $$;
drop trigger if exists social_solicitud_guard on public.social_solicitudes;
create trigger social_solicitud_guard before insert or update on public.social_solicitudes for each row execute function public.social_solicitud_guard();

-- Al bloquear: se borra la amistad y las solicitudes entre los dos.
create or replace function public.social_bloqueo_limpia() returns trigger language plpgsql security definer set search_path = public as $$
begin
  if new.quien <> auth.uid() then raise exception 'no permitido'; end if;
  delete from social_amistades where (de = new.quien and para = new.a_quien) or (de = new.a_quien and para = new.quien);
  delete from social_solicitudes s using social_partidas p where s.partida = p.id and
    ((p.autor = new.quien and s.jugador = new.a_quien) or (p.autor = new.a_quien and s.jugador = new.quien));
  return new;
end $$;
drop trigger if exists social_bloqueo_limpia on public.social_bloqueos;
create trigger social_bloqueo_limpia after insert on public.social_bloqueos for each row execute function public.social_bloqueo_limpia();

create or replace function public.social_denuncia_guard() returns trigger language plpgsql security definer set search_path = public as $$
begin
  new.quien := auth.uid(); new.revisada := false; new.creado := now();
  if (select count(*) from social_denuncias where quien = new.quien and creado > now() - interval '1 day') >= 15 then raise exception 'limite'; end if;
  return new;
end $$;
drop trigger if exists social_denuncia_guard on public.social_denuncias;
create trigger social_denuncia_guard before insert on public.social_denuncias for each row execute function public.social_denuncia_guard();

-- ───────────────────────── Permisos: solo usuarios con sesión, y solo las columnas necesarias ─────────────────────────
alter table public.social_privado     enable row level security;
alter table public.social_perfiles    enable row level security;
alter table public.social_contacto    enable row level security;
alter table public.social_amistades   enable row level security;
alter table public.social_partidas    enable row level security;
alter table public.social_solicitudes enable row level security;
alter table public.social_bloqueos    enable row level security;
alter table public.social_denuncias   enable row level security;

revoke all on public.social_privado, public.social_perfiles, public.social_contacto, public.social_amistades,
  public.social_partidas, public.social_solicitudes, public.social_bloqueos, public.social_denuncias from anon, authenticated;

grant select, insert on public.social_privado to authenticated;
-- «mayor» no se puede leer: nadie sabe si otro jugador es menor de edad.
grant select (user_id, nombre, hcp, provincia, campos, bio, visible, creado, actualizado) on public.social_perfiles to authenticated;
grant insert (user_id, nombre, hcp, provincia, campos, bio, visible), update (user_id, nombre, hcp, provincia, campos, bio, visible), delete on public.social_perfiles to authenticated;
grant select, insert, update (user_id, whatsapp, email, publico), delete on public.social_contacto to authenticated;
grant select, insert (de, para), update (estado), delete on public.social_amistades to authenticated;
grant select, insert (campo, provincia, fecha, hora, tipo, torneo, torneo_url, plazas, hcp_min, hcp_max, nota, solo_amigos),
  update (campo, provincia, fecha, hora, tipo, torneo, torneo_url, plazas, hcp_min, hcp_max, nota, solo_amigos, cerrada), delete on public.social_partidas to authenticated;
grant select, insert (partida, jugador, mensaje), update (estado, mensaje), delete on public.social_solicitudes to authenticated;
grant select, insert (quien, a_quien), delete on public.social_bloqueos to authenticated;
grant insert (contra, partida, motivo, texto) on public.social_denuncias to authenticated;
grant execute on function public.social_mi_estado() to authenticated;
revoke execute on function public.social_mi_estado() from anon;

drop policy if exists "edad: la mía" on public.social_privado;
create policy "edad: la mía" on public.social_privado for all to authenticated
  using (user_id = (select auth.uid())) with check (user_id = (select auth.uid()));

drop policy if exists "perfiles: ver" on public.social_perfiles;
create policy "perfiles: ver" on public.social_perfiles for select to authenticated
  using (user_id = (select auth.uid()) or (not public.social_bloqueo((select auth.uid()), user_id)
         and (visible or public.social_amigos((select auth.uid()), user_id) or public.social_conectados((select auth.uid()), user_id))));
drop policy if exists "perfiles: el mío" on public.social_perfiles;
create policy "perfiles: el mío" on public.social_perfiles for insert to authenticated with check (user_id = (select auth.uid()));
drop policy if exists "perfiles: editar el mío" on public.social_perfiles;
create policy "perfiles: editar el mío" on public.social_perfiles for update to authenticated using (user_id = (select auth.uid())) with check (user_id = (select auth.uid()));
drop policy if exists "perfiles: borrar el mío" on public.social_perfiles;
create policy "perfiles: borrar el mío" on public.social_perfiles for delete to authenticated using (user_id = (select auth.uid()));

drop policy if exists "contacto: ver" on public.social_contacto;
create policy "contacto: ver" on public.social_contacto for select to authenticated
  using (user_id = (select auth.uid()) or (not public.social_bloqueo((select auth.uid()), user_id) and
         (publico or public.social_amigos((select auth.uid()), user_id) or public.social_conectados((select auth.uid()), user_id))));
drop policy if exists "contacto: el mío" on public.social_contacto;
create policy "contacto: el mío" on public.social_contacto for all to authenticated
  using (user_id = (select auth.uid())) with check (user_id = (select auth.uid()));

drop policy if exists "amistades: las mías" on public.social_amistades;
create policy "amistades: las mías" on public.social_amistades for select to authenticated using ((select auth.uid()) in (de, para));
drop policy if exists "amistades: pedir" on public.social_amistades;
create policy "amistades: pedir" on public.social_amistades for insert to authenticated with check (de = (select auth.uid()));
drop policy if exists "amistades: aceptar" on public.social_amistades;
create policy "amistades: aceptar" on public.social_amistades for update to authenticated
  using (para = (select auth.uid())) with check (para = (select auth.uid()) and estado = 'aceptada');
drop policy if exists "amistades: quitar" on public.social_amistades;
create policy "amistades: quitar" on public.social_amistades for delete to authenticated using ((select auth.uid()) in (de, para));

drop policy if exists "partidas: ver" on public.social_partidas;
create policy "partidas: ver" on public.social_partidas for select to authenticated
  using (autor = (select auth.uid()) or (not public.social_bloqueo((select auth.uid()), autor)
         and (not solo_amigos or public.social_amigos((select auth.uid()), autor))));
drop policy if exists "partidas: publicar" on public.social_partidas;
create policy "partidas: publicar" on public.social_partidas for insert to authenticated with check (true);
drop policy if exists "partidas: editar las mías" on public.social_partidas;
create policy "partidas: editar las mías" on public.social_partidas for update to authenticated using (autor = (select auth.uid())) with check (autor = (select auth.uid()));
drop policy if exists "partidas: borrar las mías" on public.social_partidas;
create policy "partidas: borrar las mías" on public.social_partidas for delete to authenticated using (autor = (select auth.uid()));

drop policy if exists "solicitudes: ver" on public.social_solicitudes;
create policy "solicitudes: ver" on public.social_solicitudes for select to authenticated
  using (jugador = (select auth.uid()) or public.social_autor(partida) = (select auth.uid())
         or (estado = 'aceptada' and public.social_ve_partida(partida)));
drop policy if exists "solicitudes: pedir" on public.social_solicitudes;
create policy "solicitudes: pedir" on public.social_solicitudes for insert to authenticated with check (jugador = (select auth.uid()));
drop policy if exists "solicitudes: responder" on public.social_solicitudes;
create policy "solicitudes: responder" on public.social_solicitudes for update to authenticated
  using (public.social_autor(partida) = (select auth.uid()) or jugador = (select auth.uid()))
  with check (public.social_autor(partida) = (select auth.uid()) or jugador = (select auth.uid()));
drop policy if exists "solicitudes: retirar" on public.social_solicitudes;
create policy "solicitudes: retirar" on public.social_solicitudes for delete to authenticated
  using (jugador = (select auth.uid()) or public.social_autor(partida) = (select auth.uid()));

drop policy if exists "bloqueos: los míos" on public.social_bloqueos;
create policy "bloqueos: los míos" on public.social_bloqueos for all to authenticated
  using (quien = (select auth.uid())) with check (quien = (select auth.uid()));

drop policy if exists "denuncias: enviar" on public.social_denuncias;
create policy "denuncias: enviar" on public.social_denuncias for insert to authenticated with check (true);
-- Las denuncias solo se leen desde el panel de Supabase (Table Editor → social_denuncias).

-- ───────────────────────── DESHACER (solo si quieres quitarlo todo) ─────────────────────────
-- drop table if exists public.social_denuncias, public.social_bloqueos, public.social_solicitudes,
--   public.social_partidas, public.social_amistades, public.social_contacto, public.social_perfiles, public.social_privado cascade;
-- drop function if exists public.social_bloqueo, public.social_amigos, public.social_conectados, public.social_tiene_perfil,
--   public.social_autor, public.social_ve_partida, public.social_mi_estado, public.social_edad_ok, public.social_perfil_guard,
--   public.social_contacto_guard, public.social_amistad_guard, public.social_partida_guard, public.social_solicitud_guard,
--   public.social_bloqueo_limpia, public.social_denuncia_guard cascade;

-- ───────────────────────── Chat de cada partida (solo quien organiza y los jugadores aceptados) ─────────────────────────
create table if not exists public.social_mensajes (
  id      bigint generated always as identity primary key,
  partida uuid not null references public.social_partidas (id) on delete cascade,
  autor   uuid not null default auth.uid() references auth.users (id) on delete cascade,
  texto   text not null check (char_length(btrim(texto)) between 1 and 500),
  creado  timestamptz not null default now()
);
create index if not exists social_mensajes_partida on public.social_mensajes (partida, id);

create or replace function public.social_en_partida(pid uuid, u uuid) returns boolean
language sql stable security definer set search_path = public as $$
  select exists (select 1 from social_partidas where id = pid and autor = u)
      or exists (select 1 from social_solicitudes where partida = pid and jugador = u and estado = 'aceptada');
$$;
create or replace function public.social_mensaje_guard() returns trigger language plpgsql security definer set search_path = public as $$
begin
  new.autor := auth.uid(); new.creado := now(); new.texto := btrim(new.texto);
  if not social_en_partida(new.partida, new.autor) then raise exception 'no permitido'; end if;
  if (select count(*) from social_mensajes where autor = new.autor and creado > now() - interval '1 hour') >= 80 then raise exception 'limite'; end if;
  return new;
end $$;
drop trigger if exists social_mensaje_guard on public.social_mensajes;
create trigger social_mensaje_guard before insert on public.social_mensajes for each row execute function public.social_mensaje_guard();

alter table public.social_mensajes enable row level security;
revoke all on public.social_mensajes from anon, authenticated;
grant select, insert (partida, texto), delete on public.social_mensajes to authenticated;
drop policy if exists "mensajes: leer" on public.social_mensajes;
create policy "mensajes: leer" on public.social_mensajes for select to authenticated using (public.social_en_partida(partida, (select auth.uid())));
drop policy if exists "mensajes: escribir" on public.social_mensajes;
create policy "mensajes: escribir" on public.social_mensajes for insert to authenticated with check (true);
drop policy if exists "mensajes: borrar los míos" on public.social_mensajes;
create policy "mensajes: borrar los míos" on public.social_mensajes for delete to authenticated using (autor = (select auth.uid()));

-- ───────────────────────── Escaparate público: partidas abiertas SIN datos personales ─────────────────────────
-- Lo único que ve quien no tiene cuenta: campo, día, tipo y plazas. Ni nombres, ni notas, ni contacto.
create or replace function public.social_escaparate()
returns table (campo text, provincia text, fecha date, hora time, tipo text, torneo text, plazas smallint, libres int, hcp_min numeric, hcp_max numeric)
language sql stable security definer set search_path = public as $$
  select p.campo, p.provincia, p.fecha, p.hora, p.tipo, p.torneo, p.plazas,
         greatest(0, p.plazas - (select count(*) from social_solicitudes s where s.partida = p.id and s.estado = 'aceptada'))::int,
         p.hcp_min, p.hcp_max
  from social_partidas p
  where p.fecha >= current_date and not p.solo_amigos and not p.cerrada
  order by p.fecha, p.hora nulls last limit 12;
$$;
grant execute on function public.social_escaparate() to anon, authenticated;
-- (Para deshacer también: drop table public.social_mensajes cascade; drop function public.social_escaparate, public.social_en_partida, public.social_mensaje_guard;)
