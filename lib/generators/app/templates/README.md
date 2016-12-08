DEV:

1. Install docker
2. Install fabric3 for python3
3. Build and start containers (long operations ~30 minutes for stub with frontend)
4. Install DB dump (if you have), migrate, createsuperuser

Quick start:
```sh
$ sudo apt-get install docker.io docker-compose (for ubuntu 16.04)
$ sudo pip3 install fabric3
$ docker-compose up
$ fab initialize (if you have db dump use "fab initialize:dump_path=*.dump/sql") 
```

AVAILABLE COMMANDS:
- all docker, docker-compose
- fab restore_backup (pg_restore/psql -U postgres -d postgres < *.dump in db container)
- fab migrate (./manage.py migrate in server container)
- fab restart (docker-compose kill && docker-compose up)
- fab stop (docker-compose kill)
- fab start (docker-compose up)
- fab createsuperuser (./manage.py createsuperuser is server container)
- fab initialize (fab migrate + fab createsuperuser + fab restart)
- fab initialize:dump_path=... (fab restore_backup + fab initialize)
- fab makemigrations
- fab makemigrations:app=APP_NAME
- fab test (./manage.py test in server container)
- fab test:coverage=html/report (fab test + create coverage report)
- fab test:test_args=apps.example_app (fab test for special app or file)
- fab bash (call bash in server container)
- fab shell (call shell in server container)

#####################

- if you need force build containers - use "docker-compose build" (for rebuild all) or "docker-compose build server/client/..."

P.S. backend start on http://localhost:8000

################################################################################

PROD:

1. Install docker
2. Install fabric3
2. FORCE build container
3. Start containers
4. Migrate DB

NOT AVAILABLE COMMANDS:
- fab initialize:dump_path=... (because db name may be different)
- fab restore_backup (same reason)

Example to restore dump:
- docker-compose stop SERVER_CONTAINER_ID CELERY_CONTAINER_ID
- docker exec -it DB_CONTAINER_ID psql -U postgres
- \l (to see database names)
- drop database NAME (if need)
- create database NAME (if need)
- docker exec -it -it DB_CONTAINER_ID pg_restore/psql -U postgres -d NAME < *.dump/sql
- docker-compose start SERVER_CONTAINER_ID CELERY_CONTAINER_ID


Example:
```sh
$ sudo apt-get install docker.io docker-compose (for ubuntu 16.04)
$ sudo pip3 install fabric3
$ docker-compose --file docker-compose.yml --file docker-compose.production.yml build
$ docker-compose --file docker-compose.yml --file docker-compose.production.yml up -d
$ fab migrate
```
