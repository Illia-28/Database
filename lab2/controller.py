import psycopg2
from config import host, user, password, db_name


def conect():
    connection = psycopg2.connect(host=host, user=user, password=password, database=db_name)
    print("PostgreSQL connect")
    return connection

def close(connection):
    connection.close()
    print("PostgreSQL connection is closed")