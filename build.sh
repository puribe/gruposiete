#!/usr/bin/env bash
# Exit on error
set -o errexit

# Modify this line as needed for your package manager (pip, poetry, etc.)
pip install -r requirements.txt

# Convert static asset files
python manage.py collectstatic --no-input

# Apply any outstanding database migrations
python manage.py migrate

# Import init custom data
python manage.py loaddata database.json

# python -m gunicorn myproject.asgi:application -k uvicorn.workers.UvicornWorker