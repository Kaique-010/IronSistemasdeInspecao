#!/bin/sh

set -e

echo "========================================"
echo " Iron Sistema de Inspeção "
echo "========================================"

echo "Aplicando migrações..."

python manage.py migrate

echo "Iniciando servidor Django..."

exec python manage.py runserver 0.0.0.0:8000