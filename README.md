# Account-fund-transfers-service-docker
Small service/app that handles fund transfers between two accounts, and inserts account records files.


## Normal Setup

The first thing to do is to clone the repository:

```sh
$ git https://github.com/Tharwat99/account-fund-transfers-service-.git
$ cd account-fund-transfers-service-
```

Create a virtual environment to install dependencies in and activate it:

```sh
$ virtualenv2 --no-site-packages env
$ source env/bin/activate
```

Then install the dependencies:

```sh
(env)$ pip install -r requirements.txt
```
Note the `(env)` in front of the prompt. This indicates that this terminal
session operates in a virtual environment set up by `virtualenv2`.

Then makemigrations and migrate models to sqlite db:
```sh
(env)$ python manage.py makemigrations 
(env)$ python manage.py migrate
```

Once `pip` has finished downloading the dependencies:

```sh
(env)$ python manage.py runserver
```
And navigate to `http://127.0.0.1:8000/`.

## Tests

To run the tests:
```sh
(env)$ python manage.py test
```
## Docker Setup

The first thing to do is to clone the repository:

```sh
$ git https://github.com/Tharwat99/account-fund-transfers-service-.git
$ cd account-fund-transfers-service-
```
Then up and build docker compose file
```sh
$ docker-compose  up --build
```
## Tests

To run the tests:
```sh
(env)$ docker-compose run app sh -c "python manage.py test"
```
## Live Docker image on DockerHub in your terminal or cmd 

```sh
$ docker run -p 8000:8000  mtharwat/transfer-refunds-django:v1
```
