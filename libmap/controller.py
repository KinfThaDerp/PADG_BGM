import os
import re
import bcrypt
import psycopg2
from dotenv import load_dotenv

load_dotenv(verbose=True)

# ─── Database ────────────────────────────────────────────────────────────────

connection = psycopg2.connect(
    dbname=os.getenv("DB_NAME"),
    user=os.getenv("DB_USERNAME"),
    password=os.getenv("DB_PASSWORD"),
    host=os.getenv("DB_HOST"),
    port=os.getenv("DB_PORT"),
)
cursor = connection.cursor()

# ─── Validation ───────────────────────────────────────────────────────────────

EMAIL_REGEX = re.compile(r"[^@]+@[^@]+\.[^@]+")


def is_valid_email(email: str) -> bool:
    return bool(EMAIL_REGEX.fullmatch(email))


# ─── Password helpers ─────────────────────────────────────────────────────────

def hash_password(password: str) -> str:
    # bcrypt automatically generates a salt and stores it in the hash
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()


def verify_password(password: str, stored_hash: str) -> bool:
    # bcrypt handles the salt automatically when verifying
    return bcrypt.checkpw(password.encode(), stored_hash.encode())


# ─── Database helpers ─────────────────────────────────────────────────────────

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
        LIMIT 1;
    """
    cursor.execute(query, (email,))
    return cursor.fetchone() is not None


def push_account_to_db(username: str, email: str, password: str) -> None:
    # Use bcrypt instead of SHA256
    password_hash = hash_password(password)

    query = """
        INSERT INTO account (username, email, password_hash)
        VALUES (%s, %s, %s);
    """
    cursor.execute(query, (username, email, password_hash))
    connection.commit()


# ─── Logic ───────────────────────────────────────────────────────────────

def register_account(
    username: str,
    email: str,
    password: str,
    confirm_password: str,
    **optional
) -> tuple[bool, str]:

    if not username or not email or not password:
        return False, "Required fields are missing."

    if not is_valid_email(email):
        return False, "Invalid email format."

    if password != confirm_password:
        return False, "Passwords do not match."

    if does_account_with_username_exist(username):
        return False, "Username already taken."

    if does_account_with_email_exist(email):
        return False, "Email already registered."

    push_account_to_db(username, email, password)
    return True, "User registered successfully."


def login_account(username: str, password: str) -> tuple[bool, str]:
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
    ok, msg = register_account(
        "KinfThaDerp",
        "bassam.grzegorz@gmail.com",
        "xd987654",
        "xd987654"
    )
    print(ok, msg)
