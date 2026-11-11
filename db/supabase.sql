-- Banderín · cuentas de usuario (Supabase, región Frankfurt)
-- Ejecutar una vez en Supabase → SQL Editor.
-- Cada persona tiene una fila con su perfil, lo que sigue, guardados, jugados y su llave de avisos.
-- La seguridad la impone la base de datos (RLS): nadie puede leer ni tocar la fila de otro.

create table if not exists public.perfiles (
  user_id     uuid primary key references auth.users (id) on delete cascade,
  datos       jsonb not null default '{}'::jsonb,
  actualizado timestamptz not null default now(),
  constraint datos_tamano check (octet_length(datos::text) < 200000)
);

alter table public.perfiles enable row level security;

drop policy if exists "leer su perfil" on public.perfiles;
drop policy if exists "crear su perfil" on public.perfiles;
drop policy if exists "editar su perfil" on public.perfiles;
create policy "leer su perfil"   on public.perfiles for select to authenticated using ((select auth.uid()) = user_id);
create policy "crear su perfil"  on public.perfiles for insert to authenticated with check ((select auth.uid()) = user_id);
create policy "editar su perfil" on public.perfiles for update to authenticated using ((select auth.uid()) = user_id) with check ((select auth.uid()) = user_id);

revoke all on public.perfiles from anon;
grant select, insert, update on public.perfiles to authenticated;

-- Borrar la propia cuenta (y con ella su fila de perfiles, por el ON DELETE CASCADE).
create or replace function public.borrar_mi_cuenta()
returns void
language plpgsql
security definer
set search_path = ''
as $$
begin
  if auth.uid() is null then
    raise exception 'sin sesión';
  end if;
  delete from auth.users where id = auth.uid();
end;
$$;

revoke all on function public.borrar_mi_cuenta() from public, anon;
grant execute on function public.borrar_mi_cuenta() to authenticated;
