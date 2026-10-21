#!/bin/sh
# Перевірка відновлення: розгортає останню копію в окрему тимчасову БД
# і порівнює кількість записів у ключових таблицях з робочою БД.
# Запуск: docker compose exec backup sh /scripts/restore_check.sh
set -eu
LATEST=$(ls -1t /backups/*.dump 2>/dev/null | head -n 1 || true)
if [ -z "$LATEST" ]; then
    echo "Немає жодної резервної копії в /backups" >&2
    exit 1
fi
CHECK_DB="${PGDATABASE}_restore_check"
echo "Перевіряю копію: $LATEST"
dropdb --if-exists "$CHECK_DB"
createdb "$CHECK_DB"
pg_restore --no-owner --dbname="$CHECK_DB" "$LATEST"

STATUS=0
for TABLE in users_user medical_patientprofile medical_doctorprofile medical_medicalrecord access_control_accessgrant; do
    LIVE=$(psql -d "$PGDATABASE" -tAc "SELECT count(*) FROM $TABLE")
    RESTORED=$(psql -d "$CHECK_DB" -tAc "SELECT count(*) FROM $TABLE")
    echo "$TABLE: робоча БД=$LIVE, відновлена=$RESTORED"
    if [ "$LIVE" != "$RESTORED" ]; then STATUS=1; fi
done
dropdb "$CHECK_DB"

if [ "$STATUS" -eq 0 ]; then
    echo "Відновлення успішне: кількість записів збігається."
else
    echo "Увага: є розбіжності (можливо, дані змінилися після створення копії)." >&2
fi
exit "$STATUS"
