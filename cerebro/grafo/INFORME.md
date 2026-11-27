<!-- Generado por tools/brain_build.py (tools/grafo.py). No editar a mano. -->
# Informe del grafo de conocimiento

Cómo está conectado el cerebro de Varios: qué sostiene todo, qué temas forman grupos, qué conecta temas distintos, qué falta y qué preguntas conviene hacerse. Se regenera con el cerebro (D-018); no forma parte del grafo.

## Resumen

- 570 nodos: seccion 412, documento 88, habilidad 20, decision 16, agente 13, proceso 12, departamento 5, fuente 4.
- 491 relaciones: 80 % EXTRACTADAS (escritas en la fuente), 20 % INFERIDAS (temas compartidos, con puntuación) y 0 AMBIGUAS (para revisar).
- 11 comunidades de temas.

## Nodos centrales

Lo que más cosas conecta. Si cambia, cambia mucho.

1. **Informe del grafo de conocimiento** (`cerebro/grafo/INFORME.md`) · 41 conexiones
2. **Equipo de agentes de Banderín** (`agentes/README.md`) · 24 conexiones
3. **Registro de decisiones** (`cerebro/decisiones.md`) · 22 conexiones
4. **Atención a usuarios** (`agentes/equipo/atencion.md`) · 19 conexiones
5. **Cerebro de Banderín** (`cerebro/README.md`) · 19 conexiones
6. **Reglas de todo el equipo** (`agentes/REGLAS.md`) · 18 conexiones
7. **Comercial y alianzas** (`agentes/equipo/comercial.md`) · 18 conexiones
8. **Estratega de producto** (`agentes/equipo/estratega.md`) · 18 conexiones
9. **Redes sociales** (`agentes/equipo/redes.md`) · 17 conexiones
10. **Estado del equipo** (`agentes/ESTADO.md`) · 16 conexiones
11. **Operaciones (vigilante)** (`agentes/equipo/operaciones.md`) · 16 conexiones
12. **Analista y estratega de negocio** (`agentes/equipo/analista.md`) · 15 conexiones

## Puentes entre temas

Nodos por los que pasa el camino entre comunidades distintas (intermediación).

- **Informe del grafo de conocimiento** · intermediación 0.327 · une la comunidad 5 con 1, 2, 3, 4, 6, 7
- **Registro de decisiones** · intermediación 0.13 · une la comunidad 4 con 1, 3, 5
- **Equipo de agentes de Banderín** · intermediación 0.106 · une la comunidad 7 con 1, 2, 3, 5, 6, 8
- **Atención a usuarios** · intermediación 0.1 · une la comunidad 9 con 0, 1, 2, 3, 5, 6
- **Redes sociales** · intermediación 0.097 · une la comunidad 6 con 0, 1, 5, 7, 10
- **Estratega de producto** · intermediación 0.087 · une la comunidad 2 con 1, 3, 5, 7, 9, 10
- **Analista y estratega de negocio** · intermediación 0.085 · une la comunidad 1 con 0, 3, 5, 7, 9, 10
- **Cerebro de Banderín** · intermediación 0.078 · une la comunidad 3 con 1, 4, 5, 6, 7, 8
- **Comercial y alianzas** · intermediación 0.076 · une la comunidad 3 con 0, 1, 5, 6, 7, 9
- **Posicionamiento en Google** · intermediación 0.058 · une la comunidad 10 con 0, 1, 2, 3, 5, 7

## Conexiones sorprendentes

Secciones de carpetas y comunidades distintas que tratan lo mismo y no se enlazan. Relación INFERIDA: compruébala.

- `agentes/equipo/operaciones.md` › Operaciones (vigilante)  ↔  `cerebro/grafo/INFORME.md` › 9 · agentes/habilidades · Operaciones (vigilante) y Memoria · Operaciones (vigilante)  [INFERIDA 0.75]
- `agentes/equipo/redes.md` › Redes sociales  ↔  `cerebro/grafo/INFORME.md` › 6 · agentes/habilidades · Redes sociales y Tarea · Redes sociales (martes, jueves y sábado, 10:23)  [INFERIDA 0.75]
- `agentes/README.md` › Cómo funciona  ↔  `cerebro/procesos.md` › Procesos de Banderín  [INFERIDA 0.75]
- `agentes/memoria/operaciones.md` › Lecciones  ↔  `cerebro/01-fuentes-y-acuerdos.md` › RFEG (rfegolf.es)  [INFERIDA 0.75]
- `agentes/tareas/README.md` › Automatizaciones sin IA (GitHub Actions, gratis, sin tokens)  ↔  `cerebro/02-arquitectura.md` › Seguridad y copias  [INFERIDA 0.75]
- `agentes/tareas/redes.md` › Tarea · Redes sociales (martes, jueves y sábado, 10:23)  ↔  `cerebro/grafo/INFORME.md` › 6 · agentes/habilidades · Redes sociales y Tarea · Redes sociales (martes, jueves y sábado, 10:23)  [INFERIDA 0.75]
- `agentes/equipo/atencion.md` › Cómo trabaja  ↔  `cerebro/grafo/INFORME.md` › 8 · agentes/habilidades · Atención a usuarios y Triaje de correo  [INFERIDA 0.75]

## Comunidades

### 0 · Agentes de la oficina · Analista y estratega de negocio y Operaciones (vigilante)

Cohesión 0.18 · 26 nodos: Analista y estratega de negocio; Operaciones (vigilante); Redes sociales; Leer y citar el cerebro; Comercial y alianzas; Atención a usuarios; Separar hecho, hipótesis y propuesta; Calidad y revisión (y 18 más)

### 1 · agentes/equipo · Reglas de todo el equipo y Analista y estratega de negocio

Cohesión 0.18 · 21 nodos: Reglas de todo el equipo; Analista y estratega de negocio; Estado del equipo; Leer y citar el cerebro; Legal y privacidad; Separar hecho, hipótesis y propuesta; Calidad y revisión; Director de Banderín (y 13 más)

### 2 · agentes/habilidades · Estratega de producto y Estratega de producto

Cohesión 0.22 · 17 nodos: Estratega de producto; Estratega de producto; Desarrollo web; Desarrollo web; Arreglar con cuidado; Tarea semanal · Estratega (jueves 10:51); Arreglar con cuidado; Construir una propuesta aprobada (y 9 más)

### 3 · cerebro · Comercial y alianzas y Cerebro de Banderín

Cohesión 0.18 · 17 nodos: Comercial y alianzas; Cerebro de Banderín; 02 · Arquitectura; Banderín · contexto para Claude; 03 · Producto (lo que puede hacer un usuario hoy); Tarea · Comercial (días 8 y 22, 11:43); Oportunidades comerciales y alianzas; Prospección (y 9 más)

### 4 · cerebro · Registro de decisiones y D-011 · Ubicación de clubes desde `club_ubicacion.json`

Cohesión 0.12 · 16 nodos: Registro de decisiones; D-011 · Ubicación de clubes desde `club_ubicacion.json`; D-010 · Golf Directo autoriza el bot (Griñón, 11:10); D-015 · Las mejoras de la web las propone el estratega y solo se construyen con el «ok» de Juan; D-001 · Web estática en Cloudflare Pages + datos generados por GitHub Actions; D-002 · Respetar siempre robots.txt y no suplantar navegadores; D-003 · Avisos por correo con doble confirmación (D1 + Brevo); D-004 · Repositorios públicos con licencia (Actions gratis) (y 8 más)

### 5 · cerebro/grafo · Informe del grafo de conocimiento y Procesos de Banderín

Cohesión 0.25 · 15 nodos: Informe del grafo de conocimiento; Procesos de Banderín; D-016 · Meta: 300 suscriptores activos antes del 1/03/2027; P01 · Actualizar torneos; P02 · Avisos por correo; P03 · Salud; P04 · Métricas semanales; P05 · Vigilancia de seguridad (y 7 más)

### 6 · agentes/habilidades · Redes sociales y Tarea · Redes sociales (martes, jueves y sábado, 10:23)

Cohesión 0.29 · 12 nodos: Redes sociales; Tarea · Redes sociales (martes, jueves y sábado, 10:23); 06 · Redes sociales; Voz de Banderín; 05 · Marca y voz; Motor de reels de Banderín; Programar en Metricool; Hacer un reel (y 4 más)

### 7 · agentes · Equipo de agentes de Banderín y Arranque y cierre común de todas las tareas programadas

Cohesión 0.33 · 9 nodos: Equipo de agentes de Banderín; Arranque y cierre común de todas las tareas programadas; 07 · Métricas; Tareas programadas de los agentes; Tarea semanal · Analista (lunes 08:16); Preguntas para Juan; Datos de la semana 2026-W48; Pendientes de montaje (y 1 más)

### 8 · agentes/habilidades · Operaciones (vigilante) y Memoria · Operaciones (vigilante)

Cohesión 0.43 · 7 nodos: Operaciones (vigilante); Memoria · Operaciones (vigilante); Tarea · Operaciones (lunes y jueves, 07:47); Abrir una incidencia; Comprobar la salud de Banderín; 09 · Riesgos; Comprobar la salud de Banderín

### 9 · agentes/habilidades · Atención a usuarios y Triaje de correo

Cohesión 0.33 · 7 nodos: Atención a usuarios; Triaje de correo; Tarea · Atención (lunes y jueves, 09:13); Borrador de correo; Triaje de correo; Casos de atención y respuestas que ya funcionan; Memoria · Atención a usuarios

### 10 · agentes/habilidades · Posicionamiento en Google y Registrar y aprender

Cohesión 0.5 · 5 nodos: Posicionamiento en Google; Registrar y aprender; Tarea · Posicionamiento (días 1 y 15, 11:07); Mejora de posicionamiento; Memoria · Posicionamiento en Google

## Huecos

- **Documentos sin ninguna relación** (2): `agentes/incidencias/README.md`; `marketing/reels/IDEAS.md`
- **Decisiones que no cita ninguna sección** (0): ninguna
- **Procesos sin especialista responsable** (12): P01, P02, P03, P04, P05, P06, P07, P08, P09, P10, P11, P12
- **Fuentes registradas que nadie cita** (4): F-FED, F-GD, F-NC, F-RFEG
- **Referencias rotas** (se citan pero no existen): D-018 ×3
- **Enlaces ambiguos** (un nombre de archivo con varios destinos): 0

## Preguntas sugeridas

_Preguntas que este grafo ayuda a responder o que conviene decidir:_

- **¿Por qué «Informe del grafo de conocimiento» conecta la comunidad 5 con las comunidades 1, 2, 3, 4?**
  _Intermediación alta (0.327): es un puente entre temas._
- **¿Por qué «Registro de decisiones» conecta la comunidad 4 con las comunidades 1, 3, 5?**
  _Intermediación alta (0.13): es un puente entre temas._
- **¿Por qué «Equipo de agentes de Banderín» conecta la comunidad 7 con las comunidades 1, 2, 3, 5?**
  _Intermediación alta (0.106): es un puente entre temas._
- **¿Se aprueba D-016 · Meta: 300 suscriptores activos antes del 1/03/2027? Sigue en propuesta y la citan 4 secciones.**
  _Una decisión en propuesta que ya sostiene mucho contenido._
- **¿Deberían enlazarse «agentes/equipo/operaciones.md» y «cerebro/grafo/INFORME.md»?**
  _Tratan lo mismo (relación INFERIDA 0.75) pero no se citan._
- **¿Deberían enlazarse «agentes/equipo/redes.md» y «cerebro/grafo/INFORME.md»?**
  _Tratan lo mismo (relación INFERIDA 0.75) pero no se citan._
- **¿Qué es D-018? Se menciona 3 veces pero no existe en el registro.**
  _Referencia rota._

## Cómo usarlo

- En la oficina, cada agente recibe las secciones que encajan con su encargo **y lo conectado a ellas** (decisiones, procesos, fuentes y secciones relacionadas), con la etiqueta de confianza de cada relación.
- En local: `python3 tools/grafo.py consulta "pregunta"`, `camino "A" "B"` y `explica "X"`.
- Las relaciones INFERIDAS son pistas, no hechos: si una es buena, conviértela en un enlace en el documento y pasará a EXTRACTADA.
