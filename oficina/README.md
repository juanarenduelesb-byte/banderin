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
