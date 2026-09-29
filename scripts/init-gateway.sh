#!/bin/sh
set -eu
echo "Total estimated capacity: ~165M tokens/day"
echo "Minimum ~130M/day | Maximum ~270M/day"
echo "30 Sep expansion target: ~190-205M/day"
exec python3 /scripts/gateway-init.py
