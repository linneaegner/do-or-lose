#!/usr/bin/env bash
# Stable run script — no hot reload (breaks Flet web in Cursor)
set -e
cd "$(dirname "$0")"
source .venv/bin/activate

PORT=8550
if lsof -ti:"$PORT" >/dev/null 2>&1; then
  echo "Stoppar gammal process på port $PORT..."
  kill $(lsof -ti:"$PORT") 2>/dev/null || true
  sleep 1
fi

echo "Startar Förfest på http://127.0.0.1:$PORT"
echo "Öppna den adressen i webbläsaren (inte bara Simple Browser om det strular)."
flet run main.py -w -p "$PORT" --host 127.0.0.1
