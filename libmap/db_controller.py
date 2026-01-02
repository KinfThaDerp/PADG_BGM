import psycopg2

db_connection = psycopg2.connect(
    "dbname=postgres",
    user="postgres",
    password="postgres",
    host="localhost",
    port=5432)

db_cursor = db_connection.cursor()

if __name__ == '__main__':
    print("Running from init file")