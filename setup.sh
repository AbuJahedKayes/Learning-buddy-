#!/bin/bash
# setup.sh - Quick setup script for Learning Buddy

set -e

echo "Running database migrations..."
python manage.py migrate

echo "Creating superuser (if not exists)..."
python manage.py shell -c "
from django.contrib.auth.models import User
if not User.objects.filter(username='admin').exists():
    User.objects.create_superuser('admin', 'admin@example.com', 'admin')
    print('Superuser created: admin/admin')
else:
    print('Superuser already exists')
"

echo "Setup complete!"
echo "Access the API at: http://localhost:8000/api/"
echo "Access the Admin at: http://localhost:8000/admin/"
