import re
import sqlite3

def checkName(): 
    # Sjekke at navn er på riktig format
    name = input("Skriv inn navnet ditt (Fornavn Etternavn) (exit for å avslutte): ").strip()
    name_pattern = re.compile(r'[A-Za-z]+\s+[A-Za-z]')
    #((len(name) == 0) or (len(name.split()) == 1)) 
    while (not bool(name_pattern.match(name))) and (name.lower() != "exit"):
        name = input("Du skrev ikke et gyldig navn, prøv igjen (exit for å avslutte): ")
    return name

def checkEmail(): 
    # Sjekke at epost er på riktig format
    pattern = re.compile(r'^\S+@\S+\.\S')
    email = input("Skriv inn epost (exit for å avslutte): ").strip()
    #emailSplit = email.split("@")
    while not bool(pattern.match(email)) and email.lower() != "exit":
        email = input("Du skrev ikke en gyldig epost, prøv igjen (exit for å avslutte): ")
        #emailSplit = email.split("@")
    return email

def checkTlf(): 
    # Sjekke at telefonnummer er på riktig format
    tlf = input("Skriv inn telefonnummeret ditt (8 tall) (exit for å avslutte): ").strip()
    pattern = re.compile(r'^\d{8}$')
    while (not bool(pattern.match(tlf)) and (tlf.lower() != "exit")):
        tlf = input("Du skrev ikke et gyldig telefonnummer, prøv igjen (exit for å avslutte): ")
    return tlf

def registerCustomer(con, cursor, name, email, tlf): 
    # Registrerer kunden i databasen 
    cursor.execute("INSERT INTO Kunde VALUES(NULL,?,?,?)", (name, email, tlf))
    con.commit()

def register(con, cursor):
    while True:
        # Henter ut informasjon fra bruker
        name = checkName()
        # Lar brukeren kunne avslutte registreringen 
        if name == "exit":
            print("Avbrutt")
            return

        email = checkEmail()
        # Lar brukeren kunne avslutte registreringen 
        if email == "exit":
            print("Avbrutt")
            return

        tlf = checkTlf()
        # Lar brukeren kunne avslutte registreringen 
        if tlf == "exit":
            print("Avbrutt")
            return
        tlf = int(tlf)

        # Sjekker om epost og telefonnummer er i bruk 
        checkIfUnique = cursor.execute("SELECT * FROM Kunde WHERE \"E-post\" = ? OR TelefonNr = ?", (email, tlf))
        if checkIfUnique.fetchone() != None:
            print("E-post eller telefonnummer er allerede i bruk. Prøv igjen.\n")
            continue
        else: 
            print("Kunden er registrert.")
            break 
        
    # Registerer kunden i databasen
    registerCustomer(con, cursor, name, email, tlf)

def main():
    print("Dette vil registrere en ny kunde i databasen.")
    con = sqlite3.connect("TogDB_Data.db")
    cursor = con.cursor()
    register(con, cursor)
    con.close()
