#!/usr/bin/env bash
# Stable run script — no hot reload (breaks Flet web in Cursor)
set -euo pipefail
cd "$(dirname "$0")"

PYTHON="${PYTHON:-python3}"
VENV_DIR=".venv"
VENV_PY="$VENV_DIR/bin/python"
FLET="$VENV_DIR/bin/flet"

venv_ok() {
  [[ -x "$VENV_PY" ]] || return 1
  "$VENV_PY" -c "import flet" >/dev/null 2>&1 || return 1
  [[ -x "$FLET" ]] || return 1
  "$FLET" --version >/dev/null 2>&1 || return 1
}

setup_venv() {
  echo "Skapar/uppdaterar virtual environment..."
  if [[ -d "$VENV_DIR" ]]; then
    rm -rf "$VENV_DIR"
  fi
  "$PYTHON" -m venv "$VENV_DIR"
  "$VENV_PY" -m pip install --upgrade pip
  "$VENV_PY" -m pip install -r requirements.txt
  if [[ -f requirements-dev.txt ]]; then
    "$VENV_PY" -m pip install -r requirements-dev.txt
  fi
}

if ! venv_ok; then
  setup_venv
fi

PORT=8550
if lsof -ti:"$PORT" >/dev/null 2>&1; then
  echo "Stoppar gammal process på port $PORT..."
  kill "$(lsof -ti:"$PORT")" 2>/dev/null || true
  sleep 1
fi

echo "Startar Rundan på http://127.0.0.1:$PORT"
echo "Öppna den adressen i webbläsaren (inte bara Simple Browser om det strular)."
"$FLET" run main.py -w -p "$PORT" --host 127.0.0.1
