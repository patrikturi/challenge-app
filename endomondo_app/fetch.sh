set -e
. env.sh
./virtualenv/bin/python manage.py fetch_challenges
