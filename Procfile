worker: celery worker -A csvImporter -c 4 -Q products
web: gunicorn csvImporter.wsgi