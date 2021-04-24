#! /bin/sh
set -e
rm -rf ./core/static
python ./manage.py migrate
python ./manage.py collectstatic
gunicorn core.wsgi --bind 0.0.0.0:80 -w 4
