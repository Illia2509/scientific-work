#!/bin/sh
# Щодобове резервне копіювання PostgreSQL. Запускається сервісом backup.
set -eu
mkdir -p /backups
while true; do
    sh /scripts/backup.sh
    sleep 86400
done
