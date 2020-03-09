#!/bin/bash

rm ./srv/project/run/celerybeat.pid
celery -A currency_exchange beat -l info --workdir=/srv/project/src --pidfile=/srv/project/run/celerybeat.pid