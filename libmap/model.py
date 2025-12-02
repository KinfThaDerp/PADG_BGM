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

class AddressData:
    def __init__(self, voivodeshipName, cityName:str, streetName:str, buildingNumber:str, apartmentNumber:str, latitude:float, longitude:float):
        self.voivodeship = voivodeshipName
        self.city = cityName
        self.street = streetName
        self.building = buildingNumber
        self.apartment = apartmentNumber
        self.coords = [latitude, longitude]

class Person:
    def __init__(self, name:str, surname:str, contact:ContactData, address:AddressData):
        self.name = name
        self.surname = surname
        self.contact = contact
        self.address = address

class LibraryWorker(Person):
    def __init__(self, name:str, surname:str, contact:ContactData, address:AddressData):
        super().__init__(name, surname, contact, address)

class LibraryReader(Person):
    def __init__(self, name:str, surname:str, contact:ContactData, address:AddressData):
        super().__init__(name, surname, contact, address)

class Library:
    def __init__(self, name:str, address:AddressData, contact:ContactData):
        self.name = name
        self.address = address
        self.contact = contact

class City:
    def __init__(self):
        self.name = ""
if __name__ == '__main__':
    janek = LibraryReader("Janek", "Borowski", 953123456, "email@gmail.com")
    print(janek.name, janek.surname, janek.contact.phoneNumber, janek.contact.email)