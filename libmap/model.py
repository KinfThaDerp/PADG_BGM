import libmap.controller as ctrl

people: dict[int, dict] = {}
books: dict[int, dict] = {}
libraries: dict[int, dict] = {}


def refresh_people() -> None:
    global people
    rows = ctrl.fetch_people()

    people = {
        row[0]: {
            "id": row[0],
            "account_id": row[1],
            "name": row[2],
            "surname": row[3],
            "contact_id": row[4],
            "address_id": row[5],
            "role": row[6],
        }
        for row in rows
    }


def refresh_books() -> None:
    global books
    rows = ctrl.fetch_books()

    books = {
        row[0]: {
            "id": row[0],
            "title": row[1],
            "author": row[2],
            "isbn_13": row[3],
            "publisher": row[4],
            "genre": row[5],
        }
        for row in rows
    }


def refresh_libraries() -> None:
    global libraries
    rows = ctrl.fetch_libraries()

    libraries = {
        row[0]: {
            "id": row[0],
            "name": row[1],
            "address_id": row[2],
            "contact_id": row[3],
            "city_id": row[4],
        }
        for row in rows
    }


def refresh_all() -> None:
    refresh_people()
    refresh_books()
    refresh_libraries()


def get_people_list():
    return [f"{p['name']} {p['surname']} ({p['role']})" for p in people.values()]


def get_books_list():
    return [f"{b['title']} by {b['author']}" for b in books.values()]


def get_libraries_list():
    return [l['name'] for l in libraries.values()]


if __name__ == '__main__':
    refresh_all()

    print("People:", get_people_list())
    print("Books:", get_books_list())
    print("Libraries:", get_libraries_list())
