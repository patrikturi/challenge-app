[![Build Status](https://dev.azure.com/patrikturi/endomondo-team-challenge/_apis/build/status/patrikturi.endomondo-team-challenge?branchName=master)](https://dev.azure.com/patrikturi/endomondo-team-challenge/_build/latest?definitionId=3&branchName=master)

## Introduction

This app lets you host team challenges. Teams can be set up in the admin site and competitor data is parsed from a third party service of choice.

> Example: which team ran the most kilometers this month using [Strava](https://strava.com).

**Supported data providers**:
* [Strava](https://strava.com) (In development)
* [Endomondo](http://endomondo.com) (Retired - only historical support)

## Deployment

* `git clone git@github.com:patrikturi/challenge-app.git`
* `cd challenge-app`
* Create `.env` file and fill in these secrets:
```
SECRET_KEY=
SENTRY_DSN=
STRAVA_SECRET=
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
* Check `./core/logs/` and https://sentry.io if the fetcher has any errors

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
touch ./core/db/db.sqlite3
./manage.py migrate
./manage.py test
./manage.py runserver
```
