#!/usr/bin/env python3
"""Genera cerebro/semana.md: lo que el equipo de la oficina necesita saber esta semana.

Torneos del próximo fin de semana y de los próximos 14 días (desde site/data.js), por comunidad y
provincia, cambios recientes y la última fila de métricas. Solo lista y fechas: nada de precios,
jugadores ni resultados (acuerdo con Golf Directo). Sin IA, sin tokens.

Uso: python3 agentes/tools/semana_oficina.py
"""
import csv, json, re, datetime as dt
from collections import Counter
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[2]
DATA = RAIZ / 'site' / 'data.js'
METRICAS = RAIZ / 'agentes' / 'historico' / 'metricas.csv'
SALIDA = RAIZ / 'cerebro' / 'semana.md'
DIAS = ['lunes', 'martes', 'miércoles', 'jueves', 'viernes', 'sábado', 'domingo']
MESES = ['ene', 'feb', 'mar', 'abr', 'may', 'jun', 'jul', 'ago', 'sep', 'oct', 'nov', 'dic']


def leer(nombre, s):
    m = re.search(r'window\.' + nombre + r'=(.*?);\s*\n', s, re.S)
    return json.loads(m.group(1)) if m else None


def f(d):
    return f'{DIAS[d.weekday()]} {d.day} {MESES[d.month - 1]}'


def activo(t, a, b):
    """El torneo se juega algún día entre a y b (incluidos)."""
    try:
        s = dt.date.fromisoformat(t['s'])
        e = dt.date.fromisoformat(t.get('e') or t['s'])
    except Exception:
        return False
    return s <= b and e >= a


def main():
    s = DATA.read_text(encoding='utf-8')
    T = leer('TORNEOS', s) or []
    cambios = leer('CAMBIOS', s) or []
    act = leer('ACTUALIZADO', s)
    hoy = dt.date.today()
    # Fin de semana que viene (o el actual si hoy es sábado o domingo)
    sab = hoy + dt.timedelta(days=(5 - hoy.weekday()) % 7) if hoy.weekday() != 6 else hoy - dt.timedelta(days=1)
    dom = sab + dt.timedelta(days=1)
    finde = [t for t in T if activo(t, sab, dom)]
    quince = [t for t in T if activo(t, hoy, hoy + dt.timedelta(days=14))]
    por_cc = Counter(t.get('ccaa') or 'Sin comunidad' for t in finde)
    por_prov = Counter(t.get('prov') for t in finde if t.get('prov'))
    por_cat = Counter(t.get('cat') or 'Otros' for t in finde)

    L = ['# Semana en Banderín',
         '',
         f'**Resumen: el fin de semana del {f(sab)} y {f(dom)} hay {len(finde)} torneos en juego; en los próximos 14 días, {len(quince)}; '
         f'en total en la web, {len(T)}. Comunidad con más torneos este finde: '
         f'{por_cc.most_common(1)[0][0] if por_cc else "—"} ({por_cc.most_common(1)[0][1] if por_cc else 0}).**',
         '',
         f'Generado el {f(hoy)} de {hoy.year} con los datos de la web (actualizados el {act}). '
         'Se regenera cada semana; úsalo para el contenido de redes y los avisos. '
         'Solo lista y fechas: nunca precios, jugadores ni resultados (acuerdo con Golf Directo).',
         '',
         f'## Fin de semana del {f(sab)} y {f(dom)}',
         '',
         f'- {len(finde)} torneos en juego. En los próximos 14 días: {len(quince)}. En total en la web: {len(T)}.',
         '- Por comunidad: ' + ', '.join(f'{k} {v}' for k, v in por_cc.most_common()) + '.',
         '- Provincias con más torneos: ' + ', '.join(f'{k} {v}' for k, v in por_prov.most_common(8)) + '.',
         '- Por tipo: ' + ', '.join(f'{k} {v}' for k, v in por_cat.most_common(6)) + '.',
         '',
         '## Torneos del fin de semana por comunidad',
         '']
    for cc, _ in por_cc.most_common():
        L.append(f'### {cc}')
        for t in sorted((t for t in finde if (t.get('ccaa') or 'Sin comunidad') == cc), key=lambda x: (x['s'], x['n']))[:12]:
            d = dt.date.fromisoformat(t['s'])
            lugar = ', '.join(x for x in [t.get('club'), t.get('prov')] if x)
            extra = ' · '.join(x for x in [t.get('cat'), t.get('mod')] if x)
            L.append(f'- {f(d)}: {t["n"]} ({lugar}){" · " + extra if extra else ""}')
        resto = sum(1 for t in finde if (t.get('ccaa') or 'Sin comunidad') == cc) - 12
        if resto > 0:
            L.append(f'- … y {resto} más.')
        L.append('')

    nuevos = [c for c in cambios if c.get('k') == 'nuevo'][:10]
    retirados = [c for c in cambios if c.get('k') == 'retirado'][:10]
    if nuevos or retirados:
        L += ['## Cambios recientes', '']
        L += [f'- Nuevo: {c["n"]} ({c.get("club", "")}), {c.get("s", "")}' for c in nuevos]
        L += [f'- Retirado: {c["n"]} ({c.get("club", "")})' for c in retirados]
        L.append('')

    if METRICAS.exists():
        filas = list(csv.DictReader(METRICAS.open(encoding='utf-8')))
        if filas:
            u = filas[-1]
            L += ['## Métricas de la última semana', '',
                  f'- Fecha: {u.get("fecha")}. Suscriptores activos a los avisos: {u.get("suscriptores_activos")} '
                  f'(altas esta semana: {u.get("altas_semana")}). Avisos enviados en la semana: {u.get("avisos_enviados_semana")}.',
                  '- Meta propuesta: 300 suscriptores activos. Lo que no mueva esta cifra es secundario.', '']

    L += ['## Ideas de contenido que salen de estos datos', '',
          f'- Reel o carrusel con los torneos del finde en {por_cc.most_common(1)[0][0] if por_cc else "la comunidad con más torneos"}.',
          '- Una pieza por comunidad pequeña con pocos torneos: «aunque sean pocos, están todos en banderin.es».',
          '- Recordatorio de inscripción para los torneos de dentro de 7 a 14 días (sin precios).', '']
    SALIDA.write_text('\n'.join(L), encoding='utf-8')
    print(f'{SALIDA.relative_to(RAIZ)}: finde {len(finde)} torneos, 14 días {len(quince)}')


if __name__ == '__main__':
    main()
