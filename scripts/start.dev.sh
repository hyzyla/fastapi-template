#!/bin/bash

set -euf -o pipefail

bash scripts/init.sh
exec uvicorn --factory app.main:create_app --host 0.0.0.0 --port 8009 --reload
