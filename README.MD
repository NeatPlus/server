# Neat+ server

Repository for neat+ server

### Setup
1. Create external-service docker network `docker network create external-services`
2. If server is setup for local environment than soft link `docker-compose.dev.yml` else link `docker-compose.prod.yml` for production
    - For development/testing `ln -s docker-compose.dev.yml docker-compose.yml`
    - For development/testing `ln -s docker-compose.prod.yml docker-compose.yml`
3. Create `.env` file from `.env.example` and set appropriate and required env as explained in `.env.example`
4. If either postgres or redis is required than run command `docker-compose -f external-services.yml up -d` Note: Only postgres or redis can be run by using command `docker-compose -f external-services.yml up -d <NAME>` where `<NAME>` is replaced by either `psql` or `redis`.
    - If you have setup any other database instead of sqlite3 then server needs database to be created before starting server
    - To create database run command `docker exec db psql -U postgres -c 'create database DATABASE_NAME;'.`. Replace DATABASE_NAME with actual database
5. Run `docker-compose up -d` to start both server and celery worker or `docker-compose up -d server` to start server only. To do task in background celery should be running.
6. Execute `docker-compose exec server sh` and run command `./manage.py createsuperuser` if super user is not created
7. Access server using url http://localhost:8000 and access admin using http://localhost:8000/admin
