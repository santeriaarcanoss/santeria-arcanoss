#!/usr/bin/env bash
# Genera las placas del horóscopo para las fechas indicadas y borra carpetas de más de 21 días.
# Uso (desde la raíz del repo): tools/horoscopo/generar.sh 2026-11-23 2026-11-26
set -euo pipefail
cd "$(dirname "$0")/../.."
TZ=America/Buenos_Aires node tools/horoscopo/datos.mjs public/index.html "$@" > /tmp/horoscopo-datos.json
python3 tools/horoscopo/placas.py /tmp/horoscopo-datos.json public/horoscopo
limite=$(date -d "-21 days" +%F)
for dir in public/horoscopo/*/; do
  f=$(basename "$dir"); [[ "$f" < "$limite" ]] && rm -rf "$dir" && echo "borrado $f"
done
exit 0
