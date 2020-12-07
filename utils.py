from contextlib import contextmanager
from functools import wraps
from itertools import chain, islice
from time import time

import psycopg2


def timing(f):
    @wraps(f)
    def wrap(*args, **kw):
        ts = time()
        result = f(*args, **kw)
        te = time()
        print("func:%r args:[%r, %r] took: %2.4f sec" % (f.__name__, args, kw, te - ts))
        return result

    return wrap


@contextmanager
def postgres_connector():
    conn = psycopg2.connect("dbname=test user=postgres password=test host='127.0.0.1'")
    try:
        cursor = conn.cursor()
        yield cursor
    except Exception as e:
        print(e)
    finally:
        conn.commit()
        cursor.close()
        conn.close()


def chunks(iterable, size=10):
    iterator = iter(iterable)
    for first in iterator:
        yield chain([first], islice(iterator, size - 1))
