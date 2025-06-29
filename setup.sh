#!/bin/sh
set -e
if [ ! -d .venv ]; then
    python3 -m venv .venv
    . .venv/bin/activate
    pip install --upgrade pip
    pip install -r requirements.txt
else
    . .venv/bin/activate
fi
if [ -f .env ]; then
    export $(grep -v '^#' .env | xargs)
fi
exec uvicorn fastapi_app:app --host 0.0.0.0 --port 8000
