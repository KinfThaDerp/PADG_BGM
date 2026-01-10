import os
import re
import bcrypt
import psycopg2
from dotenv import load_dotenv
from bs4 import BeautifulSoup
import requests

load_dotenv(verbose=True)

# Database

connection = psycopg2.connect(
    dbname=os.getenv("DB_NAME"),
    user=os.getenv("DB_USERNAME"),
    password=os.getenv("DB_PASSWORD"),
    host=os.getenv("DB_HOST"),
    port=os.getenv("DB_PORT"),
)
cursor = connection.cursor()




#  Validation

EMAIL_REGEX = re.compile(r"[^@]+@[^@]+\.[^@]+")


def is_valid_email(email: str) -> bool:
    return bool(EMAIL_REGEX.fullmatch(email))

def is_valid_phone_number(phone_number:int) -> bool:
    if (len(str(phone_number)) == 9 or len(str(phone_number)) == 11)  and isinstance(phone_number, int):
        return True
    else:
        return False

#  Password Hashing

def hash_password(password: str) -> str:
    # bcrypt automatically generates a salt and stores it in the hash
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()


def verify_password(password: str, stored_hash: str) -> bool:
    # bcrypt handles the salt automatically when verifying
    return bcrypt.checkpw(password.encode(), stored_hash.encode())

#  Web Scraping
header = {
            "User-Agent": "<Mozilla 5/0 (Windows NT 10.0; Win64; x64; Trident/7.0)>",
        }
def scrape_coords(location):
    url: str = f'https://pl.wikipedia.org/wiki/{location}'
    response = requests.get(url, headers=header)
    response_html = BeautifulSoup(response.content, 'html.parser')
    latitude = float((response_html.select('.latitude'))[1].text.replace(',', '.'))
    longitude = float((response_html.select('.longitude'))[1].text.replace(',', '.'))
    return latitude, longitude

def scrape_voivodeship(location):
    url: str = f'https://pl.wikipedia.org/wiki/{location}'
    response = requests.get(url, headers=header)
    response_html = BeautifulSoup(response.content, 'html.parser')

    links = response_html.find_all('a', title=True)
    for link in links:
        title = link['title']
        if title.startswith('Województwo '):
            return link.text.strip()

    return None

#  Database

def does_account_with_username_exist(username: str) -> bool:
    query = """
            SELECT 1
            FROM account
            WHERE username = %s
            LIMIT 1;
            """
    cursor.execute(query, (username,))
    return cursor.fetchone() is not None


def does_account_with_email_exist(email: str) -> bool:
    query = """
            SELECT 1
            FROM account
            WHERE email = %s
            LIMIT 1; \
            """
    cursor.execute(query, (email,))
    return cursor.fetchone() is not None


def insert_account(cursor, username: str, email: str, password: str) -> int:
    password_hash = hash_password(password)
    query = """
            INSERT INTO account (username, email, password_hash)
            VALUES (%s, %s, %s)
            RETURNING id;
            """
    cursor.execute(query, (username, email, password_hash))
    return cursor.fetchone()[0]


def insert_contact(cursor, phone_number: int | None, email: str | None ) -> int:
    query = """
            INSERT INTO contact (phoneNumber, email)
            VALUES (%s, %s)
            RETURNING id;
            """
    cursor.execute(query, (phone_number, email))
    return cursor.fetchone()[0]


def insert_address(
    cursor,
    city_id: int | None,
    street: str | None,
    building: str | None,
    apartment: str | None,
    coords: list[float] | tuple [float,float] | None
) -> int:
    query = """
            INSERT INTO address (city, street, building, apartment, coords)
            VALUES (%s, %s, %s, %s, %s)
            RETURNING id;
            """
    cursor.execute(query, (city_id, street, building, apartment, coords))
    return cursor.fetchone()[0]

def insert_person(
    cursor,
    account_id: int,
    name: str,
    surname: str,
    contact_id: int | None,
    address_id: int | None
) -> int:
    query = """
             INSERT INTO person (account, name, surname, contact, address)
             VALUES (%s, %s, %s, %s, %s)
             RETURNING id;
             """
    cursor.execute(query, (account_id, name, surname, contact_id, address_id))
    return cursor.fetchone()[0]

def simple_fetch(fetch_func, *args, **kwargs) -> list:
    original_tuple = fetch_func(*args, **kwargs)
    result = []
    for item in original_tuple:
        filtered_item = []  # Define it *once per row*
        for info in item:
            if info is not None and not (isinstance(info, int) or (isinstance(info, str) and info.isdigit())):
                filtered_item.append(info)
        result.append(filtered_item)
    return result


def fetch_people() -> list:
    query = """
            SELECT * FROM person;
            """
    cursor.execute(query)
    people = cursor.fetchall()
    return people

def fetch_books(**kwargs) -> list:
    simple = kwargs.get("simple")
    query = """
            SELECT * FROM book;
            """
    cursor.execute(query)
    books = cursor.fetchall()
    return books

def fetch_libraries(**kwargs) -> list:
    simple = kwargs.get("simple")
    query = """
            SELECT * FROM library;
            """
    cursor.execute(query)
    libraries = cursor.fetchall()
    return libraries

def fetch_city_id(name: str) -> int | None:
    if not name:
        return None
    query = """
            SELECT id
            FROM city
            WHERE name = %s
            LIMIT 1; \
            """
    cursor.execute(query, (name,))
    result = cursor.fetchone()
    return result[0] if result else None

def insert_city(cursor, name: str) -> int | None:
    if not name:
        return None

    voivodeship = scrape_voivodeship(name)
    if not voivodeship:
        voivodeship = "Unknown"

    query = """
            INSERT INTO city (name, voivodeship) 
            VALUES (%s, %s) 
            RETURNING id;
            """
    cursor.execute(query, (name, voivodeship))
    return cursor.fetchone()[0]
#  Logic

def register_account_person(
    username: str,
    email: str,
    password: str,
    confirm_password: str,
    name: str,
    surname: str,
    phone_number: int | None,
    city: str | None,
    street: str | None,
    building: str | None,
    apartment: str | None
) -> tuple[bool, str]:

    if password != confirm_password:
        return False, "Passwords do not match"

    if not is_valid_email(email):
        return False, "Invalid email format"

    try:
        with connection:
            with connection.cursor() as cursor:

                if does_account_with_username_exist(username):
                    return False, "Username already exists"

                if does_account_with_email_exist(email):
                    return False, "Email already exists"

                city_id = fetch_city_id(city)
                if city_id is None:
                    city_id = insert_city(cursor, city)

                latitude, longitude = scrape_coords("Warszawa")
                coords = [latitude, longitude]

                account_id = insert_account(cursor, username, email, password)
                contact_id = insert_contact(cursor, phone_number, email)
                address_id = insert_address(cursor,city_id,street,building,apartment, coords)

                insert_person(cursor,account_id,name,surname,contact_id,address_id)

        return True, "User registered successfully"

    except psycopg2.Error as e:
        return False, f"error: {e.pgerror}"

def login_account(
        username: str,
        password: str
) -> tuple[bool, str]:
    if not username or not password:
        return False, "Required fields are missing."

    if not does_account_with_username_exist(username):
        return False, "User doesn't exist."

    query = """
            SELECT password_hash
            FROM account
            WHERE username = %s
            LIMIT 1;
            """
    
    cursor.execute(query, (username,))
    result = cursor.fetchone()
    stored_password_hash = result[0]

    if not verify_password(password, stored_password_hash):
        return False, "Incorrect password."

    return True, "Login successful."

if __name__ == "__main__":
    # cursor = connection.cursor()
    #
    # query = "SELECT * FROM book"
    # where = " WHERE title LIKE %s"
    #
    # sql = query + where
    # param = ("%Classical Mythology%",)
    #
    # cursor.execute(sql, param)
    # result = cursor.fetchall()
    # print(result)


    print(fetch_libraries())
