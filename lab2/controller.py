import psycopg2


def conect():
    connection = psycopg2.connect(user="postgres", password="qwerty", host="localhost", port="5432", database="postgres")
    print("PostgreSQL connect")
    return connection

def close(connection):
    connection.close()
    print("PostgreSQL connection is closed")