web: gunicorn csvImporter.wsgi
worker: celery worker -A csvImporter -c 4 -Q products