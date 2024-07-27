#!/bin/bash

set -euxo pipefail

python manage.py collectstatic --no-input
python manage.py migrate --no-input
python -m celery -A codevance_api worker -l info