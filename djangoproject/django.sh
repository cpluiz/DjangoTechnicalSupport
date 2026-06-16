#!/bin/bash
echo "Create migrations"
python manage.py makemigrations ticketapi
echo "==================================="

echo "Migrate"
python manage.py migrate
echo "==================================="

echo "Populate Server"
python manage.py populate_db
echo "==================================="

echo "==================================="
echo "Start server"
python manage.py runserver 0.0.0.0:8000