# Oficina de Banderín

La oficina de agentes de Banderín, montada igual que la de empresa-IA y adaptada a un solo negocio.

## Qué hay
- `index.html`: la oficina (Inicio, Encargos, Proyectos, Clientes, Cerebro, Calendario, Agentes en 3D, Decisiones, Reunión).
- `agentes.json`: las fichas de los 13 agentes (generado).
- `brain.json`: el cerebro troceado (todos los documentos de `cerebro/`, `agentes/`, decisiones, histórico y grafo). Generado.
- `office.js`, `oficina3d.js`: la vista 3D (Three.js en `vendor/three`).
- `entregables.js` y `vendor/`: exportar entregas a Word, PowerPoint, Excel y PDF.

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
