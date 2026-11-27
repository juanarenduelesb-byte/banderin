#!/usr/bin/env bash
# Validación antes de subir cualquier cambio: datos de la web (igual que la actualización diaria) + salud rápida.
# Uso: bash agentes/tools/validar.sh   (sale con error si algo falla)
set -euo pipefail
cd "$(dirname "$0")/../.."
git fetch -q origin main || true
git show origin/main:site/data.js > /tmp/banderin_prev_data.js 2>/dev/null || cp site/data.js /tmp/banderin_prev_data.js
node pipeline/validate.mjs site/data.js site/pasados.js /tmp/banderin_prev_data.js
python3 agentes/tools/comprobar.py --rapido
echo "✅ Validación correcta"
