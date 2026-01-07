import os
import psycopg2
from dotenv import load_dotenv

load_dotenv(verbose=True)

connection = psycopg2.connect(
    dbname=os.getenv("DB_NAME"),
    user=os.getenv("DB_USERNAME"),
    password=os.getenv("DB_PASSWORD"),
    host=os.getenv("DB_HOST"),
    port=os.getenv("DB_PORT")
)

cursor = connection.cursor()

# def fetchUser():
#     print("Fetching")


if __name__ == '__main__':
    print("Running from init file")