import psycopg2
from psycopg2.extensions import connection as Connection
import threading

from config import CONN_PARAMS

class Postgress:
    _instance = None
    _lock = threading.Lock()

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            with cls._lock:
                if not cls._instance:
                    cls._instance = super(Postgress, cls).__new__(cls)
        return cls._instance

    def __init__(self):
        if not hasattr(self, 'conn'):
            self.conn = self.connect()

    @staticmethod
    def connect() -> Connection:
        return psycopg2.connect(**CONN_PARAMS)

    def fetch(self, sql, fetch=False):
        with self._lock:
            with self.conn.cursor() as cursor:
                cursor.execute(sql)

                if fetch: 
                    result = cursor.fetchall()
                    return result

if __name__ == '__main__':
    cls = Postgress()
    response = cls.fetch('SELECT * FROM films', True)
    print(response)

    