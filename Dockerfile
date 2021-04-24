FROM python:3.8.3-slim

WORKDIR /app

RUN apt-get update && apt-get -y install cron
COPY app-cron /etc/cron.d/app-cron
RUN chmod 0644 /etc/cron.d/app-cron
RUN crontab /etc/cron.d/app-cron

COPY ./cron_entrypoint.sh /cron_entrypoint.sh
RUN chmod +x /cron_entrypoint.sh
COPY ./app_entrypoint.sh /app_entrypoint.sh
RUN chmod +x /app_entrypoint.sh

COPY . .
RUN chmod 0744 manage.py

RUN pip install -r requirements.txt

ENV DJANGO_SETTINGS_MODULE=core.settings.production
