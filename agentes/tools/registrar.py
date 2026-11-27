#!/usr/bin/env python3
"""Añade una línea al histórico de ejecuciones y regenera el estado.
Uso: python3 agentes/tools/registrar.py --agente redes --resultado ok --resumen "Reel «El tiempo» programado 20:30" --dato torneos=158 --enlace https://…"""
import argparse, json, os, datetime, subprocess, sys
R = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
AG = json.load(open(os.path.join(R, 'org.json')))['agentes']
p = argparse.ArgumentParser()
p.add_argument('--agente', required=True, choices=sorted(AG))
p.add_argument('--resultado', required=True, choices=['ok', 'aviso', 'fallo'])
p.add_argument('--resumen', required=True)
p.add_argument('--dato', action='append', default=[], help='clave=valor (repetible)')
p.add_argument('--enlace', action='append', default=[])
a = p.parse_args()
e = dict(fecha=datetime.datetime.now(datetime.timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ'), agente=a.agente, resultado=a.resultado,
         resumen=a.resumen.strip(), datos=dict(x.split('=', 1) for x in a.dato if '=' in x), enlaces=a.enlace)
with open(os.path.join(R, 'historico', 'registro.jsonl'), 'a') as f: f.write(json.dumps(e, ensure_ascii=False) + '\n')
subprocess.run([sys.executable, os.path.join(R, 'tools', 'generar.py')], check=True)
print('registrado', e['fecha'], e['agente'], e['resultado'])
