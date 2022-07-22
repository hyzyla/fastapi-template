#!/bin/bash

set -euf -o pipefail

wait-for-it --service "${DATABASE_URL}"

alembic upgrade heads
