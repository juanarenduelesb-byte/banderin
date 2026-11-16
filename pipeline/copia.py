#!/usr/bin/env python3
"""Banderín - copia de seguridad de la base de datos de avisos (Cloudflare D1).

Vuelca todas las tablas a un JSON. Lo usa el workflow semanal «Copia de seguridad»,
que lo guarda como artefacto privado del repositorio durante 35 días.
  python3 pipeline/copia.py salida.json
"""
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from avisos import D1  # noqa: E402

db = D1()
tablas = [r['name'] for r in db.q("SELECT name FROM sqlite_master WHERE type = 'table' AND name NOT LIKE 'sqlite_%' AND name NOT LIKE '_cf_%'")]
out = {'esquema': db.q("SELECT name, sql FROM sqlite_master WHERE type IN ('table', 'index') AND sql IS NOT NULL AND name NOT LIKE '_cf_%'"),
       'tablas': {}}
for t in tablas:
    out['tablas'][t] = db.q('SELECT * FROM "%s"' % t.replace('"', ''))
json.dump(out, open(sys.argv[1], 'w', encoding='utf-8'), ensure_ascii=False)
print('copia: ' + ', '.join('%s %d filas' % (t, len(v)) for t, v in out['tablas'].items()))
