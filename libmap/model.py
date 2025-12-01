import re

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


class Library:
    def __init__(self, name, address, coords, phonenumber, email):
        self.name = name
        self.address = address
        self.coords = coords
        self.contact = ContactData(phonenumber, email)

class City:
    def __init__(self):
        self.name = ""

class Person:
    def __init__(self, name:str, surname:str):
        self.name = name
        self.surname = surname

class LibraryWorker(Person):
    def __init__(self, name:str, surname:str):
        super().__init__(name, surname)

class LibraryReader(Person):
    def __init__(self, name:str, surname:str):
        super().__init__(name, surname)

if __name__ == '__main__':

    ziemniak = ContactData(123456789,"bassam.grzegorz@gmail.com")
    print(ziemniak.phoneNumber, ziemniak.email)