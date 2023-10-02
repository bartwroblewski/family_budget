# Family budget

## Tech stack

Django, Django Rest Framework, SQLite

## Running development environment

* Install Docker
* Run the following command from the top directory:

`docker-compose -f docker-compose.dev.yml up --build`

## Running production environment

* Install Docker
* Create a `.env` file in the top directory with the following contents:
    > SECRET_KEY=your_production_secret_key_here
* Run the following command from the top directory:

`docker-compose -f docker-compose.prod.yml up --build`

## Running tests

After running dev or prod `docker-compose` as described above:
1. Determine your family budget app container ID with via `docker ps`
2. Enter the container with `docker exec -it yourcontainerid sh`
3. Run `python manage.py test` inside the container


