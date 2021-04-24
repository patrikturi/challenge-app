[![Build Status](https://dev.azure.com/patrikturi/endomondo-team-challenge/_apis/build/status/patrikturi.endomondo-team-challenge?branchName=master)](https://dev.azure.com/patrikturi/endomondo-team-challenge/_build/latest?definitionId=3&branchName=master)

## Description

[Endomondo](http://endomondo.com) allows users to track their fitness and health statistics with a mobile application and website.

Endomondo challenges allow users to compete based on calories burnt.

**Endomondo Team Challange** is an unofficial extension to compete in teams, not individually.

## Deployment

* `git clone git@github.com:patrikturi/endomondo-team-challenge.git`
* `cd endomondo-team-challenge`
* Create `.env` file and fill in these secrets:
```
ENDOMONDO_USER=
ENDOMONDO_PASSWORD=
SECRET_KEY=
SENTRY_DSN=
```
ENDOMONDO_USER & PASSWORD: login credentials to endomondo.com. SECRET_KEY: generate a key [here](https://miniwebtool.com/django-secret-key-generator/) and copy it. SENTRY_DSN: copy it from https://sentry.io -> Settings -> Client Keys (DSN) -> DSN - it is a special link to the sentry server.
* Install `docker` and `docker-compose`
* Execute:
```
sudo su
./rebuild.sh
./restart.sh
```
* http://localhost should be up and running
* Check `./projects/logs/` and https://sentry.io if the fetcher has any errors

## Administration

* Create new admin user:
```
sudo docker ps
sudo docker exec -it <container id> /app/manage.py createsuperuser
```
* Log in at https://localhost/admin
* Follow admin guide [here](docs/admin-guide.md)

## Updating deployment to new version

```
git pull
sudo su
./rebuild.sh
./restart.sh
```

## Development
* Create `.env` file same as in Deployment
* Install:
```
python3 -m venv virtualenv
. ./virtualenv/bin/activate
pip install -r requirements.txt
```
* Dev:
```
. env.sh
. ./virtualenv/bin/activate
touch ./project/db/db.sqlite3
./manage.py migrate
./manage.py test
./manage.py runserver
```

## Authors

Ákos Denke: Original idea/prototype

Patrik Túri: Rewrite and generalization
