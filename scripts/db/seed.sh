#!/usr/bin/env bash
set -euo pipefail

RESET="${1:-false}"

cd "$(dirname "$0")/../../api"

if [ "$RESET" = "true" ]; then
  poetry run python -c "from bank_api.db.seed import seed; seed(reset=True)"
else
  poetry run python -c "from bank_api.db.seed import seed; seed(reset=False)"
fi

echo "seed ok (reset=$RESET)"
