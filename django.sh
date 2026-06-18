#!/bin/bash
python3 -m venv apienv
source apienv/bin/activate

echo "Create migrations"
python manage.py makemigrations ticketapi
echo "==================================="

echo "Migrate"
python manage.py migrate
echo "==================================="

echo "Populate Server"
## Toggle --mock_data line comment to avoid creating mock data
python manage.py populate_db --mock_data
#python manage.py populate_db
echo "==================================="

echo "Create Spectacular SCHEMA"
echo "==================================="
python manage.py spectacular --color --file schema.yml
echo "==================================="

echo "==================================="
echo "Start server"
python manage.py runserver 0.0.0.0:8000