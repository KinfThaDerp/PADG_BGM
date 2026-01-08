import re

# ─── Hardcoded ───────────────────────────────────────────────────────────────


voivoideships = ("dolnośląskie", "kujawsko-pomorskie", "lubelskie", "lubuskie", "łódzkie", "małopolskie", "mazowieckie",
                 "opolskie", "podkarpackie", "podlaskie", "pomorskie", "śląskie", "świętokrzyskie",
                 "warmińsko-mazurskie", "wielkopolskie", "zachodniopomorskie")

# ─── Classes ───────────────────────────────────────────────────────────────

class ContactData:
    def __init__(self, number:int, email:str):
        self.phoneNumber = number
        self.check_valid_number()
        self.email = email
        self.check_valid_email()
    def check_valid_number(self):
        if (len(str(self.phoneNumber)) == 9) and isinstance(self.phoneNumber, int):
            return True
        else:
            raise Exception("Invalid Phone Number!")
    def check_valid_email(self):
        if isinstance(self.email, str) and re.match(r"[^@]+@[^@]+\.[^@]+", self.email):
            return self.email
        else:
            raise Exception("Invalid Email!")
    def get_data(self):
        return {
            "phoneNumber": self.phoneNumber,
            "email": self.email
        }


class City:
    def __init__(self, name, voivodeship:str):
        self.name = name
        self.voivodeship = voivodeship
    def get_data(self):
        return {
        "name": self.name,
        "voivodeship": self.voivodeship
        }

class AddressData:
    def __init__(self, city:City, streetName:str, buildingNumber:str, apartmentNumber:str, latitude:float, longitude:float):
        self.city = city
        self.street = streetName
        self.building = buildingNumber
        self.apartment = apartmentNumber
        self.coords = [latitude, longitude]
    def get_data(self):
        return {
            "voivodeship": self.city.voivodeship,
            "city": self.city,
            "street": self.street,
            "building": self.building,
            "apartment": self.apartment,
            "coords": self.coords
        }

class Book:
    def __init__(self, title:str, author:str, isbn:str, publisher, genre:list):
        self.title = title
        self.author = author
        self.isbn = isbn
        self.publisher = publisher
        self.genre = genre
    def get_data(self):
        return {
            "title": self.title,
            "author": self.author,
            "isbn": self.isbn,
            "publisher": self.publisher,
            "genre": self.genre
        }

class Account:
    def __init__(self, username:str, email:str, password:str):
        self.username = username
        self.email = email
    def get_data(self):
        return {
        "username": self.username,
        "email": self.email,
        }

class Person:
    def __init__(self, account:account, name:str, surname:str, contact:ContactData, address:AddressData):
        self.account = account
        self.name = name
        self.surname = surname
        self.contact = contact
        self.address = address
    def get_data(self):
        return {
            "account": self.account,
            "name": self.name,
            "surname": self.surname,
            "contact": self.contact.get_data(),
            "address": self.address.get_data()
        }

class Library:
    def __init__(self, name:str, address:AddressData, contact:ContactData):
        self.name = name
        self.address = address
        self.contact = contact
    def get_data(self):
        return {
            "name": self.name,
            "address": self.address.get_data(),
            "contact": self.contact.get_data()
        }

class BookCopy:
    def __init__(self, book:Book, barcode:int, library:Library, condition):
        self.book = Book
        self.barcode = barcode
        self.library = library
        self.condition = condition
    def get_data(self):
        return {
            "book": self.book.get_data(),
            "barcode": self.barcode,
            "library": self.library.get_data(),
            "condition": self.condition
        }


if __name__ == '__main__':
    print("Running")
    # janek = Person("JanBor321","Janek", "Borowski",
    #                ContactData(953123456, "email@gmail.com"),
    #                AddressData("Mazowieckie", "Warszawa", "Przykładowa", "43", "10", 50.21, 50.30))
    # print(janek.getData())
    # City("Warszawa", "Mazowsze")
