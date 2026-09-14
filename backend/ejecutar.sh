#!/bin/bash
cd "$(dirname "$0")"
uvicorn app.principal:aplicacion --host 0.0.0.0 --port 8000 --reload
