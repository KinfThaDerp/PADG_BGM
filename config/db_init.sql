--coords implemented as real[2]
--because the college computer didnt have postgis

DROP TABLE IF EXISTS contact CASCADE;
DROP TABLE IF EXISTS address CASCADE ;
DROP TABLE IF EXISTS book CASCADE ;
DROP TABLE IF EXISTS library CASCADE ;
DROP TABLE IF EXISTS book_copy CASCADE ;
DROP TABLE IF EXISTS City CASCADE;

CREATE TABLE contact (
    id serial PRIMARY KEY,
    phoneNumber int,
    email text UNIQUE
);

CREATE TABLE city(
    id serial PRIMARY KEY,
    name text NOT NULL,
    voivodeship text NOT NULL
);

CREATE TABLE address (
    id serial PRIMARY KEY,
    city INT REFERENCES city(id) ON DELETE SET NULL,
    street text NOT NULL,
    building text NOT NULL,
    apartment text,
    coords real[2]
);

CREATE TABLE account (
    id serial primary key,
    username text NOT NULL UNIQUE,
    email text NOT NULL,
    password_hash TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE person (
    id serial PRIMARY KEY,
    account INT REFERENCES account(id) ON DELETE SET NULL,
    name text NOT NULL,
    surname text NOT NULL,
    contact INT REFERENCES contact(id) ON DELETE SET NULL,
    address INT REFERENCES address(id) ON DELETE SET NULL
);


CREATE TABLE book (
    id serial PRIMARY KEY,
    title text NOT NULL ,
    author text NOT NULL ,
    isbn text UNIQUE,
    publisher text,
    genre text
);

CREATE TABLE library (
    id serial PRIMARY KEY ,
    name text NOT NULL ,
    address INT REFERENCES address(id) ON DELETE SET NULL,
    contact INT REFERENCES contact(id) ON DELETE SET NULL
);

CREATE TABLE book_copy (
    id serial PRIMARY KEY,
    book INT REFERENCES book(id) ON DELETE SET NULL,
    barcode int,
    library INT REFERENCES library(id) ON DELETE SET NULL,
    condition text
)




-- Join Table

-- CREATE TABLE library_book (
--     library_id INT REFERENCES library(id) ON DELETE CASCADE,
--     book_id INT REFERENCES book(id) ON DELETE CASCADE,
--     quantity INT DEFAULT 1,
--     PRIMARY KEY (library_id, book_id)
-- );