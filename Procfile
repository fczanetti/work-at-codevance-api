web: gunicorn codevance_api.wsgi
release: ./manage.py migrate --no-input
worker: python -m celery -A codevance_api worker -l info