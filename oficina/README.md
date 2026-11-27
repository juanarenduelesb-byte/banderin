# Oficina de Banderín

La oficina de agentes de Banderín, montada igual que la de empresa-IA y adaptada a un solo negocio.

## Qué hay
- `index.html`: la oficina (Inicio, Encargos, Proyectos, Clientes, Cerebro, Calendario, Agentes en 3D, Decisiones, Reunión).
- `agentes.json`: las fichas de los 13 agentes (generado).
- `brain.json`: el cerebro troceado (todos los documentos de `cerebro/`, `agentes/`, decisiones, histórico y grafo). Generado.
- `office.js`, `oficina3d.js`: la vista 3D (Three.js en `vendor/three`).
- `entregables.js` y `vendor/`: exportar entregas a Word, PowerPoint, Excel y PDF.

## Modo rápido (móvil)
En pantallas de menos de 760 px la oficina abre en modo rápido: botones grandes para plan de la semana, reel, publicación, carrusel, story y pregunta libre; pestañas Pedir, Te esperan y Hecho. La vista 3D se pausa. «Abrir la oficina completa» lleva a la de siempre. En el ordenador, los mismos botones salen encima de «Nuevo encargo».

## Para crear contenido
- **Calendario «Esta semana en redes»**: los 7 días siguientes, con lo pedido para cada día y los huecos. Tocar un hueco pide reel, publicación, carrusel o story para ese día.
- **Producir**: en cada reel, publicación, carrusel o story terminado. Copia el guion listo para pegarlo en el chat con Claude, que lo monta con el motor de reels.
- **Pestaña Equipo** (móvil): quién trabaja y en qué, y el botón «Ver la oficina en 3D».
- **Datos de la semana**: `cerebro/semana.md` (torneos del finde por comunidad, cambios y métricas) lo rehace cada día la acción «Semana para la oficina» (`agentes/tools/semana_oficina.py`, sin IA).

## Producción de verdad (vídeos e imágenes)
- Los encargos de reel, publicación, carrusel y story nacen con `prodEstado: "pendiente"`. El botón **Producir** lo pide para cualquier contenido ya escrito.
- La tarea programada **Productor** (`agentes/tareas/productor.md`, cada 2 horas de 9 a 23) los coge aunque la oficina esté cerrada: escribe el guion si falta, crea el MP4 con el motor de reels o las láminas con `marketing/carrusel/hacer.py`, los sube como archivos del artefacto y los deja en `prodMedia`.
- La oficina los enseña arriba del encargo (vídeo con reproductor, galería de láminas) con **Descargar** y **Descargar todo**.
- El Productor también hace los encargos de texto que se queden en cola más de 30 minutos con la oficina cerrada.

## Cómo se actualiza
No se edita a mano el bloque de datos de `index.html` ni los JSON:

```
python3 agentes/tools/generar.py        # agentes, departamentos, rutinas y bloque de datos
python3 agentes/tools/cerebro_build.py  # brain.json
```

Después se republica el artefacto (archivos `index.html`, `agentes.json`, `brain.json`).

## Departamentos
Dirección (ceo, analista, dec, bib) · Operaciones y usuarios (operaciones, atencion) · Crecimiento (redes, posicionamiento, comercial) · Producto (estratega, dev) · Calidad y legal (calj, leg).

## Límites
Los agentes de la oficina trabajan con el cerebro y proponen. Nada sale a terceros, nada se gasta y nada se borra sin el OK de Juan (ver `agentes/REGLAS.md`).

## Artefacto
Publicado como «Banderín · Oficina de agentes» (slug `28f41315-54cc-4837-af21-2d2dc82d2329`), privado. Capacidades: db (encargos y memoria), sample (agentes con Claude), downloads, assets, user.
