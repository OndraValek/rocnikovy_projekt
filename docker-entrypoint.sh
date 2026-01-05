#!/bin/bash
set -e

echo "Waiting for PostgreSQL to be ready..."
max_attempts=30
attempt=0
while ! nc -z db 5432; do
  attempt=$((attempt + 1))
  if [ $attempt -ge $max_attempts ]; then
    echo "PostgreSQL is not ready after $max_attempts attempts. Exiting."
    exit 1
  fi
  echo "Waiting for PostgreSQL... (attempt $attempt/$max_attempts)"
  sleep 1
done
echo "PostgreSQL is ready!"

echo "Running migrations..."
python manage.py migrate --noinput

echo "Collecting static files..."
python manage.py collectstatic --noinput

# Only create superuser in development
if [ "${DEBUG:-0}" = "1" ] || [ "${DJANGO_SETTINGS_MODULE}" = "maturitni_projekt.settings.dev" ]; then
    echo "Creating superuser if it doesn't exist..."
    python manage.py shell << EOF
from accounts.models import User
if not User.objects.filter(is_superuser=True).exists():
    User.objects.create_superuser(
        email='admin@example.com',
        username='admin',
        password='admin123',
        role='admin'
    )
    print('Superuser created: admin@example.com / admin123')
else:
    print('Superuser already exists')
EOF
else
    echo "Skipping superuser creation in production mode."
fi

echo "Starting server..."
exec "$@"

