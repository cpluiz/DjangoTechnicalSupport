#!/bin/sh

echo "Create migrations"
python manage.py makemigrations ticketapi
echo "==================================="

echo "Migrate"
python manage.py migrate
echo "==================================="

echo "Populate Server"
if [ "$MOCK_DATA" = "true" ]; then
    python manage.py populate_db --mock_data
else
    python manage.py populate_db
fi
echo "==================================="

echo "Create Spectacular SCHEMA"
echo "==================================="
python manage.py spectacular --color --file schema.yml
echo "==================================="

if [ "$TEST_DEPLOY" = "true" ]; then
    echo "==================================="
    echo "Run tests"
    python manage.py test
else
    echo "==================================="
    echo "Start server"
    python manage.py runserver 0.0.0.0:8000
fi