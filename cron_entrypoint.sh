#! /bin/sh
printenv > /etc/environment
cron -f
