<!-- Generado por agentes/tools/generar.py desde agentes/org.json. No editar a mano: cambia org.json y regenera. -->

# Arreglar con cuidado

`arreglar-con-cuidado` · **Cuándo:** Antes de cambiar código.

## Pasos

1. Reproduce el fallo o el comportamiento a cambiar.
2. Rama `agente/<id>-<tema>`.
3. Cambio mínimo. Nada de reescrituras.
4. `node pipeline/validate.mjs` y `python3 agentes/tools/comprobar.py --rapido`.
5. Si cambias la web: `python3 pipeline/seo.py` y revisa una captura en móvil (Playwright, 390×844).
6. Merge a main con mensaje claro (qué, por qué) y el pie de atribución.
7. Comprueba en producción tras 2–3 min.

## Resultado

Arreglo probado y explicado.

## Lista de control

- ¿Puedes explicar el fallo en una frase?
- ¿Has probado el caso que fallaba?

## Quién la usa

- [Operaciones (vigilante)](../equipo/operaciones.md)
- [Posicionamiento en Google](../equipo/posicionamiento.md)
- [Estratega de producto](../equipo/estratega.md)
