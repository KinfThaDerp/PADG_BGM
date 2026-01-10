import re
import controller as ctrl

people: dict[int, dict] = {}
books: dict[int, dict] = {}
libraries: dict[int, dict] = {}


def refresh_people() -> None:
    global people
    rows = ctrl.ctrl.fetch_people()

    people = {row[0]: {"id": row[0], "account": row[1], "name": row[2], "surname": row[3],
                       "contact": row[4], "address": row[5]} for row in rows}

def refresh_books() -> None:
    global books
    rows = ctrl.ctrl.fetch_books()

    books = {row[0]: {"id": row[0], "account": row[1], "name": row[2], "surname": row[3],
                       "contact": row[4], "address": row[5]} for row in rows}

def refresh_libraries() -> None:
    global libraries
    rows = ctrl.fetch_libraries()

    libraries = {row[0]: {"id": row[0], "account": row[1], "name": row[2], "surname": row[3],
                       "contact": row[4], "address": row[5]} for row in rows}


def get_people_list():
    return [f"{p['name']} {p['surname']}" for p in people.values()]

def get_books_list():
    return [f"{b['title']} by {b['author']}" for b in books.values()]

def get_libraries_list():
    return [l['name'] for l in libraries.values()]

if __name__ == '__main__':
    print("Running")
    print(people)
    print(books)
    print(libraries)
    print(ctrl.fetch_libraries())

