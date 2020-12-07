# Celery split tasks POC

## Run project

1. `$ pip install -r requirements.txt`
1. `$ docker run -d -p 5672:5672 rabbitmq:3-alpine`
1. `$ docker run -d -p 5432:5432 -e POSTGRES_PASSWORD=test -e POSTGRES_DB=test postgres:12-alpine`
1. `$ celery -A tasks worker --loglevel=INFO`
1. `$ python generate_input.py`
1. `$ python main.py`
