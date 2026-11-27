<!-- Generado por tools/brain_build.py (tools/grafo.py). No editar a mano. -->
# Informe del grafo de conocimiento

Cómo está conectado el cerebro de Varios: qué sostiene todo, qué temas forman grupos, qué conecta temas distintos, qué falta y qué preguntas conviene hacerse. Se regenera con el cerebro (D-018); no forma parte del grafo.

## Resumen

- 548 nodos: seccion 391, documento 87, habilidad 20, decision 16, agente 13, proceso 12, departamento 5, fuente 4.
- 500 relaciones: 79 % EXTRACTADAS (escritas en la fuente), 21 % INFERIDAS (temas compartidos, con puntuación) y 0 AMBIGUAS (para revisar).
- 11 comunidades de temas.

## Nodos centrales

Lo que más cosas conecta. Si cambia, cambia mucho.

1. **Informe del grafo de conocimiento** (`cerebro/grafo/INFORME.md`) · 47 conexiones
2. **Equipo de agentes de Banderín** (`agentes/README.md`) · 24 conexiones
3. **Registro de decisiones** (`cerebro/decisiones.md`) · 22 conexiones
4. **Atención a usuarios** (`agentes/equipo/atencion.md`) · 19 conexiones
5. **Cerebro de Banderín** (`cerebro/README.md`) · 19 conexiones
6. **Reglas de todo el equipo** (`agentes/REGLAS.md`) · 18 conexiones
7. **Comercial y alianzas** (`agentes/equipo/comercial.md`) · 18 conexiones
8. **Estratega de producto** (`agentes/equipo/estratega.md`) · 18 conexiones
9. **Redes sociales** (`agentes/equipo/redes.md`) · 18 conexiones
10. **Estado del equipo** (`agentes/ESTADO.md`) · 16 conexiones
11. **Operaciones (vigilante)** (`agentes/equipo/operaciones.md`) · 16 conexiones
12. **Analista y estratega de negocio** (`agentes/equipo/analista.md`) · 15 conexiones

## Puentes entre temas

Nodos por los que pasa el camino entre comunidades distintas (intermediación).

- **Informe del grafo de conocimiento** · intermediación 0.383 · une la comunidad 2 con 1, 3, 4, 5, 6, 7
- **Registro de decisiones** · intermediación 0.136 · une la comunidad 4 con 1, 2, 5
- **Comercial y alianzas** · intermediación 0.097 · une la comunidad 7 con 0, 1, 2, 3, 5, 6
- **Atención a usuarios** · intermediación 0.096 · une la comunidad 8 con 0, 1, 2, 3, 5, 6
- **Equipo de agentes de Banderín** · intermediación 0.093 · une la comunidad 5 con 1, 2, 3, 6, 7, 8
- **Redes sociales** · intermediación 0.093 · une la comunidad 6 con 0, 1, 2, 5, 10
- **Estratega de producto** · intermediación 0.085 · une la comunidad 3 con 1, 2, 5, 8, 10
- **Analista y estratega de negocio** · intermediación 0.079 · une la comunidad 1 con 0, 2, 5, 7, 8, 10
- **Cerebro de Banderín** · intermediación 0.068 · une la comunidad 5 con 1, 2, 3, 4, 6, 7
- **Posicionamiento en Google** · intermediación 0.057 · une la comunidad 10 con 0, 1, 2, 3, 5

## Conexiones sorprendentes

Secciones de carpetas y comunidades distintas que tratan lo mismo y no se enlazan. Relación INFERIDA: compruébala.

- `agentes/equipo/redes.md` › Redes sociales  ↔  `cerebro/grafo/INFORME.md` › 6 · agentes/habilidades · Redes sociales y Tarea · Redes sociales (martes, jueves y sábado, 10:23)  [INFERIDA 0.85]
- `agentes/equipo/leg.md` › Legal y privacidad  ↔  `cerebro/grafo/INFORME.md` › 8 · agentes/equipo · Reglas de todo el equipo y Legal y privacidad  [INFERIDA 0.75]
- `agentes/equipo/posicionamiento.md` › Posicionamiento en Google  ↔  `cerebro/grafo/INFORME.md` › 10 · agentes/habilidades · Posicionamiento en Google y Registrar y aprender  [INFERIDA 0.75]
- `agentes/memoria/operaciones.md` › Lecciones  ↔  `cerebro/01-fuentes-y-acuerdos.md` › RFEG (rfegolf.es)  [INFERIDA 0.75]
- `agentes/tareas/redes.md` › Tarea · Redes sociales (martes, jueves y sábado, 10:23)  ↔  `cerebro/grafo/INFORME.md` › 6 · agentes/habilidades · Redes sociales y Tarea · Redes sociales (martes, jueves y sábado, 10:23)  [INFERIDA 0.75]
- `agentes/equipo/atencion.md` › Cómo trabaja  ↔  `cerebro/grafo/INFORME.md` › 9 · agentes/habilidades · Atención a usuarios y Triaje de correo  [INFERIDA 0.75]

## Comunidades

### 0 · Agentes de la oficina · Analista y estratega de negocio y Operaciones (vigilante)

Cohesión 0.18 · 26 nodos: Analista y estratega de negocio; Operaciones (vigilante); Redes sociales; Leer y citar el cerebro; Comercial y alianzas; Atención a usuarios; Separar hecho, hipótesis y propuesta; Calidad y revisión (y 18 más)

### 1 · agentes/equipo · Reglas de todo el equipo y Analista y estratega de negocio

Cohesión 0.18 · 21 nodos: Reglas de todo el equipo; Analista y estratega de negocio; Estado del equipo; Leer y citar el cerebro; Separar hecho, hipótesis y propuesta; Legal y privacidad; Calidad y revisión; Director de Banderín (y 13 más)

### 2 · cerebro/grafo · Informe del grafo de conocimiento y Procesos de Banderín

Cohesión 0.16 · 20 nodos: Informe del grafo de conocimiento; Procesos de Banderín; P01 · Actualizar torneos; P02 · Avisos por correo; P03 · Salud; P04 · Métricas semanales; P05 · Vigilancia de seguridad; P06 · Copia de seguridad (y 12 más)

### 3 · agentes/habilidades · Estratega de producto y Estratega de producto

Cohesión 0.2 · 18 nodos: Estratega de producto; Estratega de producto; Desarrollo web; Desarrollo web; Arreglar con cuidado; Tarea semanal · Estratega (jueves 10:51); Arreglar con cuidado; Construir una propuesta aprobada (y 10 más)

### 4 · cerebro · Registro de decisiones y D-011 · Ubicación de clubes desde `club_ubicacion.json`

Cohesión 0.12 · 17 nodos: Registro de decisiones; D-011 · Ubicación de clubes desde `club_ubicacion.json`; D-010 · Golf Directo autoriza el bot (Griñón, 11:10); D-015 · Las mejoras de la web las propone el estratega y solo se construyen con el «ok» de Juan; D-016 · Meta: 300 suscriptores activos antes del 1/03/2027; D-001 · Web estática en Cloudflare Pages + datos generados por GitHub Actions; D-002 · Respetar siempre robots.txt y no suplantar navegadores; D-003 · Avisos por correo con doble confirmación (D1 + Brevo) (y 9 más)

### 5 · cerebro · Equipo de agentes de Banderín y Cerebro de Banderín

Cohesión 0.25 · 15 nodos: Equipo de agentes de Banderín; Cerebro de Banderín; Arranque y cierre común de todas las tareas programadas; 02 · Arquitectura; Tareas programadas de los agentes; Banderín · contexto para Claude; 07 · Métricas; 03 · Producto (lo que puede hacer un usuario hoy) (y 7 más)

### 6 · agentes/habilidades · Redes sociales y Tarea · Redes sociales (martes, jueves y sábado, 10:23)

Cohesión 0.3 · 12 nodos: Redes sociales; Tarea · Redes sociales (martes, jueves y sábado, 10:23); 06 · Redes sociales; Voz de Banderín; 05 · Marca y voz; Motor de reels de Banderín; Hacer un reel; Programar en Metricool (y 4 más)

### 7 · cerebro · Comercial y alianzas y Tarea · Comercial (días 8 y 22, 11:43)

Cohesión 0.31 · 9 nodos: Comercial y alianzas; Tarea · Comercial (días 8 y 22, 11:43); Prospección; Oportunidades comerciales y alianzas; 08 · Negocio; 00 · Qué es Banderín; Prospección; Bandeja de salida (borradores) (y 1 más)

### 8 · agentes/habilidades · Atención a usuarios y Triaje de correo

Cohesión 0.33 · 7 nodos: Atención a usuarios; Triaje de correo; Tarea · Atención (lunes y jueves, 09:13); Borrador de correo; Triaje de correo; Casos de atención y respuestas que ya funcionan; Memoria · Atención a usuarios

### 9 · agentes/habilidades · Operaciones (vigilante) y Memoria · Operaciones (vigilante)

Cohesión 0.43 · 7 nodos: Operaciones (vigilante); Memoria · Operaciones (vigilante); Tarea · Operaciones (lunes y jueves, 07:47); Abrir una incidencia; Comprobar la salud de Banderín; 09 · Riesgos; Comprobar la salud de Banderín

### 10 · agentes/habilidades · Posicionamiento en Google y Registrar y aprender

Cohesión 0.5 · 5 nodos: Posicionamiento en Google; Registrar y aprender; Tarea · Posicionamiento (días 1 y 15, 11:07); Mejora de posicionamiento; Memoria · Posicionamiento en Google

## Huecos

- **Documentos sin ninguna relación** (0): ninguno
- **Decisiones que no cita ninguna sección** (0): ninguna
- **Procesos sin especialista responsable** (12): P01, P02, P03, P04, P05, P06, P07, P08, P09, P10, P11, P12
- **Fuentes registradas que nadie cita** (0): ninguna
- **Referencias rotas** (se citan pero no existen): D-018 ×1
- **Enlaces ambiguos** (un nombre de archivo con varios destinos): 0

## Preguntas sugeridas

_Preguntas que este grafo ayuda a responder o que conviene decidir:_

- **¿Por qué «Informe del grafo de conocimiento» conecta la comunidad 2 con las comunidades 1, 3, 4, 5?**
  _Intermediación alta (0.383): es un puente entre temas._
- **¿Por qué «Registro de decisiones» conecta la comunidad 4 con las comunidades 1, 2, 5?**
  _Intermediación alta (0.136): es un puente entre temas._
- **¿Por qué «Comercial y alianzas» conecta la comunidad 7 con las comunidades 0, 1, 2, 3?**
  _Intermediación alta (0.097): es un puente entre temas._
- **¿Se aprueba D-016 · Meta: 300 suscriptores activos antes del 1/03/2027? Sigue en propuesta y la citan 3 secciones.**
  _Una decisión en propuesta que ya sostiene mucho contenido._
- **¿Deberían enlazarse «agentes/equipo/redes.md» y «cerebro/grafo/INFORME.md»?**
  _Tratan lo mismo (relación INFERIDA 0.85) pero no se citan._
- **¿Deberían enlazarse «agentes/equipo/leg.md» y «cerebro/grafo/INFORME.md»?**
  _Tratan lo mismo (relación INFERIDA 0.75) pero no se citan._
- **¿Qué es D-018? Se menciona 1 veces pero no existe en el registro.**
  _Referencia rota._

## Cómo usarlo

- En la oficina, cada agente recibe las secciones que encajan con su encargo **y lo conectado a ellas** (decisiones, procesos, fuentes y secciones relacionadas), con la etiqueta de confianza de cada relación.
- En local: `python3 tools/grafo.py consulta "pregunta"`, `camino "A" "B"` y `explica "X"`.
- Las relaciones INFERIDAS son pistas, no hechos: si una es buena, conviértela en un enlace en el documento y pasará a EXTRACTADA.
