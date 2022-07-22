#!/bin/bash

set -euf -o pipefail

exec uvicorn --factory app.main:create_app --host 0.0.0.0 --port 8000
