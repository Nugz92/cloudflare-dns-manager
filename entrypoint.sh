#!/bin/bash

mkdir -p logs
echo "[INFO] Starting Supercronic cron scheduler..."
exec /usr/local/bin/supercronic /app/schedule.cron
