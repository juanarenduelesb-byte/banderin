<!-- Generado por tools/brain_build.py (tools/grafo.py). No editar a mano. -->
# Informe del grafo de conocimiento

Cómo está conectado el cerebro de Varios: qué sostiene todo, qué temas forman grupos, qué conecta temas distintos, qué falta y qué preguntas conviene hacerse. Se regenera con el cerebro (D-018); no forma parte del grafo.

## Resumen

- 581 nodos: seccion 420, documento 89, habilidad 20, decision 18, agente 13, proceso 12, departamento 5, fuente 4.
- 507 relaciones: 80 % EXTRACTADAS (escritas en la fuente), 20 % INFERIDAS (temas compartidos, con puntuación) y 0 AMBIGUAS (para revisar).
- 11 comunidades de temas.

## Nodos centrales

Lo que más cosas conecta. Si cambia, cambia mucho.

1. **Informe del grafo de conocimiento** (`cerebro/grafo/INFORME.md`) · 40 conexiones
2. **Equipo de agentes de Banderín** (`agentes/README.md`) · 24 conexiones
3. **Registro de decisiones** (`cerebro/decisiones.md`) · 24 conexiones
4. **Atención a usuarios** (`agentes/equipo/atencion.md`) · 19 conexiones
5. **Cerebro de Banderín** (`cerebro/README.md`) · 19 conexiones
6. **Reglas de todo el equipo** (`agentes/REGLAS.md`) · 18 conexiones
7. **Comercial y alianzas** (`agentes/equipo/comercial.md`) · 18 conexiones
8. **Estratega de producto** (`agentes/equipo/estratega.md`) · 18 conexiones
9. **Operaciones (vigilante)** (`agentes/equipo/operaciones.md`) · 17 conexiones
10. **Redes sociales** (`agentes/equipo/redes.md`) · 17 conexiones
11. **Estado del equipo** (`agentes/ESTADO.md`) · 16 conexiones
12. **Analista y estratega de negocio** (`agentes/equipo/analista.md`) · 15 conexiones

## Puentes entre temas

Nodos por los que pasa el camino entre comunidades distintas (intermediación).

- **Informe del grafo de conocimiento** · intermediación 0.317 · une la comunidad 5 con 1, 2, 3, 4, 6, 7
- **Registro de decisiones** · intermediación 0.149 · une la comunidad 2 con 1, 3, 4, 5
- **Equipo de agentes de Banderín** · intermediación 0.1 · une la comunidad 7 con 1, 3, 4, 5, 6, 8
- **Atención a usuarios** · intermediación 0.098 · une la comunidad 9 con 0, 1, 3, 4, 5, 6
- **Estratega de producto** · intermediación 0.091 · une la comunidad 1 con 3, 4, 5, 7, 8, 9
- **Redes sociales** · intermediación 0.084 · une la comunidad 6 con 0, 1, 4, 5, 7, 10
- **Comercial y alianzas** · intermediación 0.082 · une la comunidad 3 con 0, 1, 4, 5, 6, 7
- **Analista y estratega de negocio** · intermediación 0.082 · une la comunidad 8 con 0, 1, 3, 4, 5, 7
- **Cerebro de Banderín** · intermediación 0.073 · une la comunidad 3 con 1, 2, 4, 5, 6, 7
- **Posicionamiento en Google** · intermediación 0.057 · une la comunidad 10 con 0, 1, 3, 4, 5, 7

## Conexiones sorprendentes

Secciones de carpetas y comunidades distintas que tratan lo mismo y no se enlazan. Relación INFERIDA: compruébala.

- `agentes/equipo/posicionamiento.md` › Posicionamiento en Google  ↔  `cerebro/grafo/INFORME.md` › 10 · agentes/habilidades · Posicionamiento en Google y Registrar y aprender  [INFERIDA 0.75]
- `agentes/README.md` › Cómo funciona  ↔  `cerebro/procesos.md` › Procesos de Banderín  [INFERIDA 0.75]
- `agentes/memoria/operaciones.md` › Lecciones  ↔  `cerebro/01-fuentes-y-acuerdos.md` › RFEG (rfegolf.es)  [INFERIDA 0.75]
- `agentes/tareas/README.md` › Automatizaciones sin IA (GitHub Actions, gratis, sin tokens)  ↔  `cerebro/02-arquitectura.md` › Seguridad y copias  [INFERIDA 0.75]
- `agentes/tareas/atencion.md` › Tarea · Atención (lunes y jueves, 09:13)  ↔  `cerebro/grafo/INFORME.md` › 9 · agentes/habilidades · Atención a usuarios y Tarea · Atención (lunes y jueves, 09:13)  [INFERIDA 0.75]
- `agentes/equipo/analista.md` › Analista y estratega de negocio  ↔  `cerebro/grafo/INFORME.md` › 8 · agentes/habilidades · Analista y estratega de negocio y Separar hecho, hipótesis y propuesta  [INFERIDA 0.75]
- `agentes/equipo/atencion.md` › Atención a usuarios  ↔  `cerebro/grafo/INFORME.md` › 9 · agentes/habilidades · Atención a usuarios y Tarea · Atención (lunes y jueves, 09:13)  [INFERIDA 0.75]

## Comunidades

### 0 · Habilidades · Analista y estratega de negocio y Operaciones (vigilante)

Cohesión 0.17 · 27 nodos: Analista y estratega de negocio; Operaciones (vigilante); Redes sociales; Leer y citar el cerebro; Comercial y alianzas; Atención a usuarios; Separar hecho, hipótesis y propuesta; Calidad y revisión (y 19 más)

### 1 · agentes/habilidades · Estratega de producto y Estado del equipo

Cohesión 0.19 · 19 nodos: Estratega de producto; Estado del equipo; Estratega de producto; Desarrollo web; Desarrollo web; Banderín · contexto para Claude; Arreglar con cuidado; Tarea semanal · Estratega (jueves 10:51) (y 11 más)

### 2 · cerebro · Registro de decisiones y D-018 · Las piezas para Instagram de Banderín se programan solas en Metricool

Cohesión 0.12 · 19 nodos: Registro de decisiones; D-018 · Las piezas para Instagram de Banderín se programan solas en Metricool; D-014 · Ningún agente escribe a terceros ni borra datos de usuarios; D-011 · Ubicación de clubes desde `club_ubicacion.json`; D-016 · Meta: 300 suscriptores activos antes del 1/03/2027; D-010 · Golf Directo autoriza el bot (Griñón, 11:10); D-015 · Las mejoras de la web las propone el estratega y solo se construyen con el «ok» de Juan; D-001 · Web estática en Cloudflare Pages + datos generados por GitHub Actions (y 11 más)

### 3 · cerebro · Comercial y alianzas y Cerebro de Banderín

Cohesión 0.19 · 16 nodos: Comercial y alianzas; Cerebro de Banderín; 02 · Arquitectura; Tarea · Comercial (días 8 y 22, 11:43); 03 · Producto (lo que puede hacer un usuario hoy); Oportunidades comerciales y alianzas; Prospección; 04 · Audiencia y mercado (y 8 más)

### 4 · agentes/equipo · Reglas de todo el equipo y Leer y citar el cerebro

Cohesión 0.2 · 14 nodos: Reglas de todo el equipo; Leer y citar el cerebro; Legal y privacidad; 01 · Fuentes y acuerdos; Calidad y revisión; Director de Banderín; Registro de decisiones; Bibliotecario (y 6 más)

### 5 · cerebro/grafo · Informe del grafo de conocimiento y Procesos de Banderín

Cohesión 0.27 · 14 nodos: Informe del grafo de conocimiento; Procesos de Banderín; P01 · Actualizar torneos; P02 · Avisos por correo; P03 · Salud; P04 · Métricas semanales; P05 · Vigilancia de seguridad; P06 · Copia de seguridad (y 6 más)

### 6 · agentes/habilidades · Redes sociales y Tarea · Productor de la oficina (a las 9, 15 y 21)

Cohesión 0.33 · 13 nodos: Redes sociales; Tarea · Productor de la oficina (a las 9, 15 y 21); Tarea · Redes sociales (martes, jueves y sábado, 10:23); Voz de Banderín; Hacer un reel; Motor de reels de Banderín; Controles antes de publicar; 06 · Redes sociales (y 5 más)

### 7 · agentes/tareas · Equipo de agentes de Banderín y Operaciones (vigilante)

Cohesión 0.31 · 11 nodos: Equipo de agentes de Banderín; Operaciones (vigilante); Arranque y cierre común de todas las tareas programadas; Tareas programadas de los agentes; Memoria · Operaciones (vigilante); Tarea · Operaciones (lunes y jueves, 07:47); Abrir una incidencia; Preguntas para Juan (y 3 más)

### 8 · agentes/habilidades · Analista y estratega de negocio y Separar hecho, hipótesis y propuesta

Cohesión 0.24 · 10 nodos: Analista y estratega de negocio; Separar hecho, hipótesis y propuesta; 07 · Métricas; Tarea semanal · Analista (lunes 08:16); Tres decisiones para Juan; Datos de la semana 2026-W48; Pendientes de montaje; Informe semanal (y 2 más)

### 9 · agentes/habilidades · Atención a usuarios y Tarea · Atención (lunes y jueves, 09:13)

Cohesión 0.33 · 7 nodos: Atención a usuarios; Tarea · Atención (lunes y jueves, 09:13); Triaje de correo; Borrador de correo; Triaje de correo; Casos de atención y respuestas que ya funcionan; Memoria · Atención a usuarios

### 10 · agentes/habilidades · Posicionamiento en Google y Registrar y aprender

Cohesión 0.5 · 5 nodos: Posicionamiento en Google; Registrar y aprender; Tarea · Posicionamiento (días 1 y 15, 11:07); Mejora de posicionamiento; Memoria · Posicionamiento en Google

## Huecos

- **Documentos sin ninguna relación** (2): `agentes/incidencias/README.md`; `marketing/reels/IDEAS.md`
- **Decisiones que no cita ninguna sección** (0): ninguna
- **Procesos sin especialista responsable** (12): P01, P02, P03, P04, P05, P06, P07, P08, P09, P10, P11, P12
- **Fuentes registradas que nadie cita** (4): F-FED, F-GD, F-NC, F-RFEG
- **Referencias rotas** (se citan pero no existen): ninguna
- **Enlaces ambiguos** (un nombre de archivo con varios destinos): 0

## Preguntas sugeridas

_Preguntas que este grafo ayuda a responder o que conviene decidir:_

- **¿Por qué «Informe del grafo de conocimiento» conecta la comunidad 5 con las comunidades 1, 2, 3, 4?**
  _Intermediación alta (0.317): es un puente entre temas._
- **¿Por qué «Registro de decisiones» conecta la comunidad 2 con las comunidades 1, 3, 4, 5?**
  _Intermediación alta (0.149): es un puente entre temas._
- **¿Por qué «Equipo de agentes de Banderín» conecta la comunidad 7 con las comunidades 1, 3, 4, 5?**
  _Intermediación alta (0.1): es un puente entre temas._
- **¿Se aprueba D-016 · Meta: 300 suscriptores activos antes del 1/03/2027? Sigue en propuesta y la citan 4 secciones.**
  _Una decisión en propuesta que ya sostiene mucho contenido._
- **¿Deberían enlazarse «agentes/equipo/posicionamiento.md» y «cerebro/grafo/INFORME.md»?**
  _Tratan lo mismo (relación INFERIDA 0.75) pero no se citan._
- **¿Deberían enlazarse «agentes/README.md» y «cerebro/procesos.md»?**
  _Tratan lo mismo (relación INFERIDA 0.75) pero no se citan._

## Cómo usarlo

- En la oficina, cada agente recibe las secciones que encajan con su encargo **y lo conectado a ellas** (decisiones, procesos, fuentes y secciones relacionadas), con la etiqueta de confianza de cada relación.
- En local: `python3 tools/grafo.py consulta "pregunta"`, `camino "A" "B"` y `explica "X"`.
- Las relaciones INFERIDAS son pistas, no hechos: si una es buena, conviértela en un enlace en el documento y pasará a EXTRACTADA.
