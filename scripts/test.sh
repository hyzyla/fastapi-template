#!/bin/bash

set -euf -o pipefail

bash scripts/init.sh

pytest "$@"
