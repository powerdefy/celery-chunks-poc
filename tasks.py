from celery import Celery

from utils import postgres_connector

app = Celery("tasks", backend="rpc://", broker="pyamqp://guest@localhost//")


@app.task
def worker_task(rows):
    with postgres_connector() as c:
        for row in rows:
            query = "INSERT INTO contacts (first_name, last_name) VALUES(%s, %s)"
            c.execute(query, (row["first_name"], row["last_name"]))
