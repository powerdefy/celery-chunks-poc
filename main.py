import csv

from celery import group

from tasks import worker_task
from utils import chunks, postgres_connector, timing


def main():
    create_contacts_table()
    normal_import()

    create_contacts_table()
    celery_import()


@timing
def normal_import():
    with open("test.csv") as csv_file:
        reader = csv.DictReader(csv_file)
        with postgres_connector() as c:
            for row in reader:
                query = "INSERT INTO contacts (first_name, last_name) VALUES(%s, %s)"
                c.execute(query, (row["first_name"], row["last_name"]))


@timing
def celery_import():
    with open("test.csv") as csv_file:
        reader = csv.DictReader(csv_file)
        csv_chunks = chunks(reader, 1000)
        g = group([worker_task.s(list(c)) for c in csv_chunks]).apply_async()
        g.get()


def create_contacts_table():
    with postgres_connector() as c:
        query = "DROP TABLE IF EXISTS contacts;"
        c.execute(query)

        query = """
        CREATE TABLE contacts (
            contact_id SERIAL PRIMARY KEY,
            first_name VARCHAR ( 50 ) NOT NULL,
            last_name VARCHAR ( 50 ) NOT NULL
        );
        """
        c.execute(query)


if __name__ == "__main__":
    main()
