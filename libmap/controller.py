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

# Database - Inserters

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
            INSERT INTO contact (phone_number, email)
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
            INSERT INTO address (city_id, street, building, apartment, coords)
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
    address_id: int | None,
    role: str = 'client'
) -> int:
    query = """
        INSERT INTO person (account_id, name, surname, contact_id, address_id, role)
        VALUES (%s, %s, %s, %s, %s, %s)
        RETURNING id;
    """
    cursor.execute(query, (account_id, name, surname, contact_id, address_id, role))
    return cursor.fetchone()[0]

def insert_city(cursor, name: str) -> int | None:
    if not name:
        return None

    voivodeship = scrape_voivodeship(name) or "Unknown"

    try:
        coords = scrape_coords(name)  # (lat, lon)
    except Exception as e:
        print(f"Failed to get coordinates for '{name}': {e}")
        return None

    query = """
        INSERT INTO city (name, voivodeship, coords) 
        VALUES (%s, %s, ARRAY[%s, %s]::real[])
        RETURNING id;
    """
    cursor.execute(query, (name, voivodeship, coords[0], coords[1]))
    return cursor.fetchone()[0]

def assign_employee_to_library(cursor, person_id: int, library_id: int) -> None:
    query = """
        INSERT INTO library_employee (person_id, library_id)
        VALUES (%s, %s)
        ON CONFLICT (person_id, library_id) DO NOTHING;
    """
    cursor.execute(query, (person_id, library_id))

# Database - Updates

def update_person(cursor, person_id: int, **kwargs) -> None:
    query = """
            UPDATE person SET {} WHERE id = %s;
            """.format(
            ", ".join(f"{key} = %s" for key in kwargs.keys())
                )
    cursor.execute(query, (*kwargs.values(), person_id))

# Database - Fetchers

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


def fetch_people(role: str | None = None) -> list:
    query = """
            SELECT id, account_id, name, surname, contact_id, address_id, role 
            FROM person"""
    if role:
        query += " WHERE role = %s"
        cursor.execute(query, (role,))
    else:
        cursor.execute(query)
    return cursor.fetchall()

def fetch_person(person_id: int) -> tuple[int, int, str, str, int | None, int | None, str]:
    query = """
            SELECT id, account_id, name, surname, contact_id, address_id, role 
            FROM person WHERE id = %s; \
            """
    cursor.execute(query, (person_id,))
    return cursor.fetchone()

def fetch_books() -> list:
    query = """
            SELECT * FROM book;
            """
    cursor.execute(query)
    books = cursor.fetchall()
    return books

def fetch_libraries() -> list:
    query = """
        SELECT id, name, address_id, contact_id, city_id
        FROM library;
    """
    cursor.execute(query)
    return cursor.fetchall()

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

def fetch_person_id(name: str, surname: str) -> int | None:
    query = """
        SELECT id
        FROM person
        WHERE name = %s AND surname = %s
        LIMIT 1;
    """
    cursor.execute(query, (name, surname))
    result = cursor.fetchone()
    return result[0] if result else None

def fetch_city(person_id: int) -> str | None:
    query = """
            SELECT city.name
            FROM person JOIN address ON person.address_id = address.id JOIN city ON address.city_id = city.id
            WHERE person.id = %s; \
            """
    cursor.execute(query, (person_id,))
    result = cursor.fetchone()
    return result[0] if result else None

def fetch_address(address_id: int) -> tuple[str, str, str, str, list[float]]:
    query = """
        SELECT city.name, address.street, address.building, address.apartment, address.coords
        FROM address
        JOIN city ON address.city_id = city.id
        WHERE address.id = %s;
    """
    cursor.execute(query, (address_id,))
    result = cursor.fetchone()
    return result if result else (None, None, None, None, None)


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
,   model=None) -> tuple[bool, str]:

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

                try:
                    latitude, longitude = scrape_coords(city)
                except Exception:
                    return False, "Invalid city"
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
) -> tuple[bool, str, int | None]:
    if not username or not password:
        return False, "Required fields are missing.", None

    if not does_account_with_username_exist(username):
        return False, "User doesn't exist.", None

    query = """
            SELECT id, password_hash
            FROM account
            WHERE username = %s
            LIMIT 1;
            """

    cursor.execute(query, (username,))
    result = cursor.fetchone()
    account_id, stored_password_hash = result[0], result[1]
    print(account_id)
    print(stored_password_hash)

    if not verify_password(password, stored_password_hash):
        return False, "Incorrect password.", None


    return True, "Login successful.", account_id

# CRUD - Person

def add_person(
    name: str,
    surname: str,
    account_id: int | None,
    phone_number: str | int | None = None,
    email: str | None = None,
    city: str | None = None,
    street: str | None = None,
    building: str | None = None,
    apartment: str | None = None,
    role: str = 'client',
) -> tuple[bool, str]:

    if not name or not surname:
        return False, "Name and surname are required"

    if role not in ("employee", "client"):
        return False, "Invalid role"

    try:
        with connection:
            with connection.cursor() as cursor:

                # City
                city_id = fetch_city_id(city)
                if city and city_id is None:
                    city_id = insert_city(cursor, city)

                coords = None
                if city:
                    try:
                        coords = list(scrape_coords(city))
                    except Exception:
                        return False, "Invalid city"

                contact_id = insert_contact(cursor, phone_number, email)
                address_id = insert_address(cursor,city_id,street,building,apartment,coords)
                insert_person(cursor,account_id,name,surname,contact_id,address_id,role)

        return True, "Person added successfully"

    except psycopg2.Error as e:
        return False, f"Database error: {e.pgerror}"

def edit_person(
    person_id: int,
    name: str | None = None,
    surname: str | None = None,
    phone_number: str | int | None = None,
    email: str | None = None,
    city: str | None = None,
    street: str | None = None,
    building: str | None = None,
    apartment: str | None = None,
) -> tuple[bool, str]:
    try:
        with connection:
            with connection.cursor() as cursor:
                cursor.execute("""
                    SELECT name, surname, contact_id, address_id
                    FROM person
                    WHERE id = %s
                    LIMIT 1;
                """, (person_id,))
                person = cursor.fetchone()
                if not person:
                    return False, "Person not found"

                old_name, old_surname, contact_id, address_id = person

                cursor.execute("""
                    SELECT phone_number, email
                    FROM contact
                    WHERE id = %s
                    LIMIT 1;
                """, (contact_id,))
                contact = cursor.fetchone()
                old_phone, old_email = contact if contact else (None, None)

                cursor.execute("""
                    SELECT city.name, address.street, address.building, address.apartment, address.coords
                    FROM address
                    JOIN city ON address.city_id = city.id
                    WHERE address.id = %s;
                """, (address_id,))
                address = cursor.fetchone()
                old_city, old_street, old_building, old_apartment, old_coords = (
                    address if address else (None, None, None, None, None)
                )

                update_person(cursor, person_id,
                              name=name if name is not None else old_name,
                              surname=surname if surname is not None else old_surname)

                new_phone = phone_number if phone_number is not None else old_phone
                new_email = email if email is not None else old_email
                if (new_phone != old_phone) or (new_email != old_email):
                    cursor.execute("""
                        UPDATE contact
                        SET phone_number = %s,
                            email = %s
                        WHERE id = %s;
                    """, (new_phone, new_email, contact_id))

                if city is not None:
                    city_id = fetch_city_id(city)
                    if city_id is None:
                        city_id = insert_city(cursor, city)
                    try:
                        coords = list(scrape_coords(city))
                    except Exception:
                        coords = old_coords
                else:
                    city_id = fetch_city_id(old_city)
                    coords = old_coords

                cursor.execute("""
                    UPDATE address
                    SET city_id = %s,
                        street = %s,
                        building = %s,
                        apartment = %s,
                        coords = %s
                    WHERE id = %s;
                """, (
                    city_id,
                    street if street is not None else old_street,
                    building if building is not None else old_building,
                    apartment if apartment is not None else old_apartment,
                    coords,
                    address_id
                ))

        return True, "Person updated successfully"

    except psycopg2.Error as e:
        return False, f"Database error: {e.pgerror}"
    except Exception as e:
        return False, str(e)

def get_person_info(person_id: int) -> dict | None:

    try:
        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT id, account_id, name, surname, contact_id, address_id, role
                FROM person
                WHERE id = %s
                LIMIT 1;
            """, (person_id,))
            person = cursor.fetchone()
            if not person:
                return None

            person_dict = {
                "id": person[0],
                "account_id": person[1],
                "name": person[2],
                "surname": person[3],
                "contact_id": person[4],
                "address_id": person[5],
                "role": person[6]
            }

            contact_id = person_dict["contact_id"]
            if contact_id:
                cursor.execute("SELECT phone_number, email FROM contact WHERE id = %s", (contact_id,))
                contact = cursor.fetchone()
                if contact:
                    person_dict["phone_number"], person_dict["email"] = contact
                else:
                    person_dict["phone_number"], person_dict["email"] = None, None
            else:
                person_dict["phone_number"], person_dict["email"] = None, None

            address_id = person_dict["address_id"]
            if address_id:
                cursor.execute("""
                    SELECT city.name, address.street, address.building, address.apartment, address.coords
                    FROM address
                    JOIN city ON address.city_id = city.id
                    WHERE address.id = %s;
                """, (address_id,))
                addr = cursor.fetchone()
                if addr:
                    person_dict["city"], person_dict["street"], person_dict["building"], person_dict["apartment"], person_dict["coords"] = addr
                else:
                    person_dict["city"], person_dict["street"], person_dict["building"], person_dict["apartment"], person_dict["coords"] = (None, None, None, None, None)
            else:
                person_dict["city"], person_dict["street"], person_dict["building"], person_dict["apartment"], person_dict["coords"] = (None, None, None, None, None)

            return person_dict

    except Exception as e:
        print(f"Error fetching person info: {e}")
        return None


def delete_person(person_id: int) -> tuple[bool, str]:
    try:
        with connection:
            with connection.cursor() as cursor:
                cursor.execute("SELECT contact_id, address_id FROM person WHERE id = %s", (person_id,))
                result = cursor.fetchone()
                if not result:
                    return False, "Person not found"
                contact_id, address_id = result

                cursor.execute("DELETE FROM person WHERE id = %s", (person_id,))
                if contact_id:
                    cursor.execute("DELETE FROM contact WHERE id = %s", (contact_id,))
                if address_id:
                    cursor.execute("DELETE FROM address WHERE id = %s", (address_id,))

        return True, "Person deleted successfully"
    except Exception as e:
        return False, f"Failed to delete person: {str(e)}"



if __name__ == "__main__":
    print("Running controller.py")
    # #print(fetch_people(role="client"))
    # print(update_person(cursor, 12, surname="Test"))
    # connection.commit()
    # login_account("KinfThaDerp", "lol123")
    # print("miasto", fetch_city(fetch_person_id("Bassamm", "Mandilii")))
    print(fetch_address(13))