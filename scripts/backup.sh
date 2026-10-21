#!/bin/sh
# Одна резервна копія БД у /backups і видалення копій, старших за BACKUP_KEEP_DAYS.
# Вручну: docker compose exec backup sh /scripts/backup.sh
set -eu
STAMP=$(date +%Y%m%d_%H%M%S)
FILE="/backups/${PGDATABASE}_${STAMP}.dump"
pg_dump --format=custom --file="$FILE"
echo "Резервну копію створено: $FILE"
find /backups -name "*.dump" -mtime +"${BACKUP_KEEP_DAYS:-7}" -delete
