#!/bin/sh
set -e

SECRET_FILE="/app/.secrets/django_secret_key"

if [ -f "$SECRET_FILE" ]; then
  export DJANGO_SECRET_KEY=$(cat "$SECRET_FILE")
else
  mkdir -p /app/.secrets
  DJANGO_SECRET_KEY=$(python - <<EOF
from django.core.management.utils import get_random_secret_key
print(get_random_secret_key())
EOF
)
  echo "$DJANGO_SECRET_KEY" > "$SECRET_FILE"
  chmod 600 "$SECRET_FILE"
  export DJANGO_SECRET_KEY
fi

exec gunicorn -c core/config.py core.wsgi:application