#!/bin/bash
set -e

host="$1"
shift
cmd="$@"

until mysql -h "$host" -u "$DB_USER" -p"$DB_PASSWORD" -e 'select 1' "$DB_NAME"; do
  >&2 echo "MySQL is unavailable - sleeping"
  sleep 5
done

>&2 echo "MySQL is up - executing command"
exec $cmd