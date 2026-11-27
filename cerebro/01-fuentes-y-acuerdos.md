# 01 · Fuentes y acuerdos

Regla general (HECHO, `pipeline/red.py`): Banderín lee con el agente `BanderinBot`, respeta el robots.txt de cada
web, hace pausas de 0,5 s y **nunca se hace pasar por un navegador**. Si un robots.txt no deja leer algo, no se lee.

## Golf Directo (golfdirecto.com) — la fuente más importante y la más delicada
- Aporta unos 830 de los torneos (≈ 75 %).
- **Acuerdo con Juan Manuel Griñón (director técnico), noviembre de 2026**, por correo:
  - Solo se lee la **lista pública de torneos** (`/api/v2/public/tournament/last`) y la de **clubes** (`/api/v2/public/club`).
  - Solo se muestran fechas del torneo y de inscripción. **Nada de precios, jugadores ni resultados.**
  - «golfdirecto.com» debe verse **claramente a la derecha del nombre del torneo** y en su ficha.
  - Se quitó toda la sección de resultados de la web.
  - 26/11/2026 11:10: «el robots.txt se actualizará por la tarde, pero ya puedes lanzar el bot».
- En `red.py` hay un permiso escrito para esas dos rutas **que caduca el 3/12/2026**. Desde ese día manda su robots.txt.
  El agente de operaciones debe comprobar antes de esa fecha que el robots.txt de Golf Directo permite a BanderinBot esas rutas.
- Si Golf Directo deja de estar disponible, sus torneos se congelan con la última copia (`pipeline/datos/gd_congelado.json`), sin precios.
- **Nunca**: escribir a Golf Directo sin que Juan apruebe el texto; mencionar que se quitan torneos; pedir reuniones (Juan no quiere).

## NextCaddy
- Unos 540 torneos (clubes que usan NextCaddy). Lectura de listas públicas (`nc_lists.py`, `nc_tours.py`, `nc_clubs.py`).

## Federaciones
- Catalana, Valenciana, Vasca, Murcia, Riojana, Navarra, Cántabra, Castilla-La Mancha, Asturias, Andalucía… (`fed_extra.py`). Calendarios públicos.

## RFEG (rfegolf.es)
- Su robots.txt **no deja leer el directorio de clubes** a BanderinBot. Desde el 25/11 la ubicación de los clubes sale de
  `pipeline/datos/club_ubicacion.json` (451 clubes, se amplía sola). Ver decisión D-011.

## Otras
- Corporate Golf, Grow Sports y entradas manuales (`pipeline/manual.json`).
