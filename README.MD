# NEAT+ server

Repository for NEAT+ server

### Setup server

<details>
<summary> Setup using docker-compose </summary>

1. Create external-service docker network `docker network create external-services`
2. If server is setup for local environment than soft link `docker/docker-compose.dev.yml` else link `docker/docker-compose.prod.yml` for production
    - For development/testing `ln -s docker/docker-compose.dev.yml docker-compose.yml`
    - For staging/production `ln -s docker/docker-compose.prod.yml docker-compose.yml`
3. Create `.env` file from `.env.example` and set appropriate and required env as explained in `.env.example`
4. If either postgres or redis is required than run command `ln -s docker/external_services.yml external_services.yml` and  `docker-compose -f external_services.yml up -d` Note: Only postgres or redis can be run by using command `docker-compose -f external_services.yml up -d <NAME>` where `<NAME>` is replaced by either `db` or `redis` respectively.
    - If you have setup any other database instead of sqlite3 then server needs database to be created before starting server
    - To create database run command `docker exec db psql -U postgres -c 'create database DATABASE_NAME;'.`. Replace DATABASE_NAME with actual database
5. Run `docker-compose up -d` to start both server and celery worker or `docker-compose up -d server` to start server only. To do task in background celery should be running.
6. Execute `docker-compose exec server sh` and run command `./manage.py createsuperuser` if super user is not created
7. Access server using url http://localhost:8000 and access admin using http://localhost:8000/admin
</details>

### Translation
NEAT+ officially support English, French and Spanish. To translate NEAT+ visit [Hosted Weblate](https://hosted.weblate.org/projects/neatplus/server/)

### License
Project is licensed using GNU GPL v3
