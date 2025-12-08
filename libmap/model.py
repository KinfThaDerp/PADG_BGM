import re

voivoideships = ("dolnośląskie", "kujawsko-pomorskie", "lubelskie", "lubuskie", "łódzkie", "małopolskie", "mazowieckie",
                 "opolskie", "podkarpackie", "podlaskie", "pomorskie", "śląskie", "świętokrzyskie",
                 "warmińsko-mazurskie", "wielkopolskie", "zachodniopomorskie")


class ContactData:
    def __init__(self, number:int, email:str):
        self.phoneNumber = number
        self.checkValidNumber()
        self.email = email
        self.checkValidEmail()
    def checkValidNumber(self):
        if (len(str(self.phoneNumber)) == 9) and isinstance(self.phoneNumber, int):
            return True
        else:
            raise Exception("Invalid Phone Number!")
    def checkValidEmail(self):
        if isinstance(self.email, str) and re.match(r"[^@]+@[^@]+\.[^@]+", self.email):
            return self.email
        else:
            raise Exception("Invalid Email!")
    def getData(self):
        return {
            "phoneNumber": self.phoneNumber,
            "email": self.email
        }

class AddressData:
    def __init__(self, voivodeshipName, cityName:str, streetName:str, buildingNumber:str, apartmentNumber:str, latitude:float, longitude:float):
        self.voivodeship = voivodeshipName
        self.city = cityName
        self.street = streetName
        self.building = buildingNumber
        self.apartment = apartmentNumber
        self.coords = [latitude, longitude]
    def getData(self):
        return {
            "voivodeship": self.voivodeship,
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

class Person:
    def __init__(self, username:str, name:str, surname:str, contact:ContactData, address:AddressData):
        self.username = username
        self.name = name
        self.surname = surname
        self.contact = contact
        self.address = address

class Library:
    def __init__(self, name:str, address:AddressData, contact:ContactData):
        self.name = name
        self.address = address
        self.contact = contact

class BookCopy:
    def __init__(self, book:Book, barcode:int, library:Library, condition):
        self.book = Book
        self.barcode = barcode
        self.library = library
        self.condition = condition


class City:
    def __init__(self):
        self.name = ""

if __name__ == '__main__':
    janek = Person("JanBor321","Janek", "Borowski",
                   ContactData(953123456, "email@gmail.com"),
                   AddressData("Mazowieckie", "Warszawa", "Przykładowa", "43", "10", 50.21, 50.30))
    print(janek.name, janek.surname)
    print(janek.contact.getData())
    print(janek.address.getData())