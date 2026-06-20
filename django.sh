#!/bin/sh

# Run initial non-root application setup here if needed
echo "Running entrypoint tasks as: $(whoami)"
echo "==================================="

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

echo "==================================="
echo "Start server"
python manage.py runserver 0.0.0.0:8000

time=$(date)
echo "::set-output name=time::$time"