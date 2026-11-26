#!/bin/bash
# Actualización completa de Banderín. Uso: bash update.sh /ruta/de/salida/data.js
set -e
OUT=${1:-/home/claude/banderin/data.js}
mkdir -p /home/claude/raw/nc /home/claude/raw/nct /home/claude/raw/gd /home/claude/raw/fed /home/claude/raw/rfegc
rm -f /home/claude/raw/nc/*.html /home/claude/raw/nct/*.html /home/claude/raw/rfegc/*.html
cd /home/claude/scr
python3 -I nc_clubs.py
python3 -I nc_lists.py
python3 -I nc_tours.py
# Golf Directo: solo la lista pública de torneos y la de clubes, si su robots.txt lo permite (gd_fetch.py lo comprueba).
# Mientras lo prohíba, sus torneos salen de pipeline/datos/gd_congelado.json (ver emit.py).
python3 -I gd_fetch.py || echo "AVISO: Golf Directo no se ha leído"
python3 -I red.py get https://www.golfdirecto.com/api/v2/public/club /home/claude/raw/gd/clubs.json || echo "AVISO: clubes de Golf Directo no leídos"
python3 -I red.py get "https://golfcv.com/wp-json/bt_ws/v1/torneos_lt/?criterio=PROXIMOS&conlimit=no&nomas=si&ordentipo=asc&limite=500&lang=0" /home/claude/raw/fed/cv.json
python3 -I rfeg_clubs.py
python3 -I fed_extra.py || echo "AVISO: calendarios federativos fallaron"
python3 -I build.py
BANDERIN_PAUSA=0.25 python3 -I check.py | head -20
python3 -I emit.py "$OUT" "${2:-}"
