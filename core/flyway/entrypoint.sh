#!/usr/bin/env bash
set -e
declare -A DBS=(
  [auth]=$AUTH_DB
)

for svc in "${!DBS[@]}"; do
  db="${DBS[$svc]}"
  echo "Migrating $svc → $db"
  flyway \
    -url="jdbc:postgresql://${POSTGRES_HOST}:${POSTGRES_PORT}/${db}" \
    -user="${POSTGRES_MIGRATIONS_USER}" \
    -password="${POSTGRES_MIGRATIONS_PASSWORD}" \
    -schemas="${db}" \
    -locations="filesystem:/flyway/sql/${svc}" \
    -baselineOnMigrate=true \
    migrate
done
