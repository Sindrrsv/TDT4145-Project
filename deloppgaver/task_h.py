import sqlite3
import datetime


def getFutureOrders(cursor, tlf):
    dagens_dato = datetime.date.today()
    # Henter ut alle fremtidige billetter for en kunde
    cursor.execute(
        """SELECT BillettNr, VognNr, SeteNr, SengNr, TogTurDato, TogTurId, StrekningNavn, Avgangstid
        FROM Billett JOIN KundeOrdre USING(OrdreNr) JOIN Kunde USING(KundeNr) JOIN (
                    SELECT StrekningNavn, Avgangstid
                    FROM KjoererDelstrekning) USING(StrekningNavn)
        WHERE TelefonNr = ? AND TogTurDato >= ? 
        ORDER BY TogTurID, TogTurDato, Avgangstid""", (tlf, dagens_dato))
    futureOrders = cursor.fetchall()
    return futureOrders


def printFutureOrders(futureOrders):
    # Presenterer fremtidige billetter på en ryddig måte
    if (len(futureOrders) == 0):
        print("Ingen fremtidige billetter funnet.")
    else:
        for order in futureOrders:
            if (order[2] == None):
                print(f"Rute {order[5]}. Dato: {order[4]}. VognNr: {order[1]}, SengNr: {order[3]}. \n\t{order[6]} med avgang: {order[7]}. (BillettNr: {order[0]})\n" )
            elif (order[3] == None):
                print(f"Rute {order[5]}. Dato: {order[4]}. VognNr: {order[1]}, SeteNr: {order[2]}. \n\t{order[6]} med avgang: {order[7]}. (BillettNr: {order[0]})\n")

def login(cursor, tlf):
    # Sjekker om kunden finnes i databasen
    cursor.execute("SELECT * FROM Kunde WHERE TelefonNr = ?", (tlf,))
    kunde = cursor.fetchall()
    if kunde:
        return True
    return False


def main():
    print("Dette vil søke etter alle fremtidige kjøp for en kunde.")
    con = sqlite3.connect("TogDB_Data.db")
    cursor = con.cursor()
    tlf = input("Skriv inn telefonnummeret ditt (8 tall/exit for å gå ut): ")
    while not login(cursor, tlf) or tlf == "exit":
        if tlf == "exit":
            print("Avbrutt")
            return
        tlf = input(
            "Telefonnummeret finnes ikke i databasen. Prøv igjen (8 tall/exit for å gå ut): ")
    printFutureOrders(getFutureOrders(cursor, tlf))

    con.close()
