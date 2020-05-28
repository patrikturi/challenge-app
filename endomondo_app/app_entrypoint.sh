#! /bin/sh
set -e
rm -rf ./project/static
python ./manage.py migrate
python ./manage.py collectstatic
gunicorn project.wsgi --bind 0.0.0.0:80 -w 4
