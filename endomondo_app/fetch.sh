set -e
PROJECT_DIR=$(dirname "$0")
. $PROJECT_DIR/env.sh
./$PROJECT_DIR/virtualenv/bin/python $PROJECT_DIR/manage.py fetch_challenges
