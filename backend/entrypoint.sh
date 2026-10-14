#!/bin/sh
set -e

# Run database migrations if AUTO_MIGRATE is not explicitly disabled
if [ "${AUTO_MIGRATE:-true}" = "true" ] || [ "${AUTO_MIGRATE:-1}" = "1" ]; then
    echo "Applying database migrations with Alembic..."
    alembic upgrade head
else
    echo "Skipping migrations (AUTO_MIGRATE=${AUTO_MIGRATE})"
fi

exec "$@"
