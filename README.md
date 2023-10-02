# Family budget

## Tech stack

Django, Django Rest Framework, SQLite, Docker

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
* Determine your family budget app container ID with via `docker ps`
* Enter the container with `docker exec -it yourcontainerid sh`
* Run `python manage.py test` inside the container

## Example usage

* Run development environment as described above
* Navigate to `localhost:8000/register` and register a user. Log in as the newly registered user (button in the top-right corner)
* Navigate to `localhost:8000/api/budgets` and create (POST) a budget
* Navigate to `localhost:8000/api/payments` and create(POST) a payment in the above budget
* Navigate to `localhost:8000/register` and register another user
* Navigate to `localhost:8000/api/budget-shares` and share (POST, still logged in as the first user) the newly created budget with the other user
* Log in as the second user
* You should see shared budgets and/or payments under `localhost:8000/api/budgets` and `localhost:8000/api/payments` respectively

