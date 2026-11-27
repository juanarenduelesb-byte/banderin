<!-- Generado por agentes/tools/generar.py desde agentes/org.json. No editar a mano: cambia org.json y regenera. -->

# Comprobar la salud de Banderín

`comprobar-salud` · **Cuándo:** Cada mañana (operaciones).

## Pasos

1. `python3 agentes/tools/comprobar.py` (sale con código 0 si todo está en verde).
2. Comprueba: actualizaciones de las últimas 24 h, torneos frente al día anterior, % sin provincia, Golf Directo leído, avisos enviados con novedades, web en línea, sitemap, permiso de Golf Directo y robots.txt.
3. Para cada fallo, mira el log de la ejecución en GitHub.

## Resultado

Lista de verdes, avisos y fallos con causa.

## Lista de control

- ¿Has comprobado el dato en producción y no solo en local?

## Quién la usa

- [Operaciones (vigilante)](../equipo/operaciones.md)
