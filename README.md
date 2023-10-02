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
