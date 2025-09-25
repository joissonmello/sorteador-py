#!/bin/sh
set -e

# Aguarda variáveis de ambiente essenciais
: "${DJANGO_SETTINGS_MODULE:?DJANGO_SETTINGS_MODULE não definido}"
: "${DATABASE_URL:?DATABASE_URL não definido}"

# Rodar migrações — opcional em produção automática, mas útil para MVP/fluxo controlado
echo "Running migrations..."
python manage.py migrate --noinput

# Coletar static files
echo "Collecting static files..."
python manage.py collectstatic --noinput

# Iniciar Gunicorn
echo "Starting Gunicorn..."
exec gunicorn config.wsgi:application \
    --bind 0.0.0.0:${PORT:-8000} \
    --workers 3 \
    --log-level info
