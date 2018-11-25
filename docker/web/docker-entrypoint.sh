#!/bin/sh
set -e

if [ "x$DJANGO_MANAGEPY_MIGRATE" = 'xon' ]; then
    rm -rf callcenterapp/migrations
    python manage.py makemigrations --noinput
    python manage.py migrate --noinput
    python manage.py makemigrations callcenterapp
    python manage.py migrate callcenterapp
fi

if [ "x$DJANGO_MANAGEPY_COLLECTSTATIC" = 'xon' ]; then
    python manage.py collectstatic --noinput
fi

if [ "x$DJANGO_CREATE_SUPERUSER" = 'xon' ]; then
    echo "============================ Creating Superuser =========================================="
    python createsuperuser.py
fi

exec "$@"