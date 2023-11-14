import sqlite3
import deloppgaver.task_h as task_h
import datetime

def getDirection(startStasjon, sluttStasjon):
    # Funksjon som finner ut om ruten går mot hovedretningen eller hovedretningen
    stations = ["Trondheim", "Steinkjer",
                "Mosjoeen", "Mo i Rana", "Fauske", "Bodoe"]
    
    # Sjekker om stasjonene eksisterer i listen over gyldige stasjoner
    if (startStasjon not in stations) or (sluttStasjon not in stations):
        return []

    # Sjekker hvilken vei ruten går
    retning = ""
    if stations.index(startStasjon) < stations.index(sluttStasjon):
        retning = "MotHovedretning"
    elif stations.index(startStasjon) > stations.index(sluttStasjon):
        retning = "Hovedretning"

    # Returenerer resultatet 
    return retning 

def getAvailableTickets(cursor, delstrekninger, dato, type):
    # Spørring for å hente ut alle billetter som er en del av ruten fra startStasjon til sluttStasjon på gitt dato
    billetter = []
    for delstrekning in delstrekninger:
        cursor.execute(f"""
        SELECT BillettNr, Billett.RuteID, VognNr, SeteNr, SengNr, OrdreNr, Delstrekning.StrekningNavn, TogTurDato, AvgangsTid, AnkomstTid, StartStasjon, SluttStasjon
        FROM Billett NATURAL JOIN Delstrekning NATURAL JOIN KjoererDelstrekning 
        WHERE Delstrekning.StrekningNavn = ? AND OrdreNr IS NULL AND TogTurDato = ? AND {type}Nr NOT NULL""", (delstrekning, dato))
        billett = cursor.fetchall()
        # Legger til alle resultatene i en liste
        billetter.append(billett)
    # Returnerer ledige billetter
    return billetter

def getSection(cursor, startStasjon, sluttStasjon, dato): 
    retning = getDirection(startStasjon, sluttStasjon)

    # Spørring for å hente ut alle delstrekninger som er en del av samme rute som startStasjon og sluttStasjon på gitt dato
    cursor.execute(f"""SELECT RuteID, StartStasjon, SluttStasjon, AvgangsTid, AnkomstTid, Dato, StrekningNavn
        FROM Togtur JOIN KjoererDelstrekning USING(RuteID) JOIN Delstrekning USING(StrekningNavn)
        WHERE RuteID = (SELECT RuteID
                        FROM Togtur JOIN KjoererDelstrekning USING(RuteID) JOIN Delstrekning USING(StrekningNavn)
                        WHERE (StartStasjon = ? OR SluttStasjon = ?) AND Dato = ? AND {retning} IS NULL
                        GROUP BY RuteID
                        HAVING COUNT (RuteID) > 1) AND Dato = ?
            OR (StartStasjon = ? AND SluttStasjon = ? AND Dato = ?)
        ORDER BY Dato, AvgangsTid""", (startStasjon, sluttStasjon, dato, dato, startStasjon, sluttStasjon, dato))
    delstrekninger = cursor.fetchall()
    
    # Lager en liste med alle delstrekninger som er en del av ruten fra startStasjon til sluttStasjon
    # Må først fjerne de delstrekningene som ikke er del av ruten fra startStasjon til sluttStasjon
    stopp = []
    for delstrekning in delstrekninger:
        if delstrekning[1] == startStasjon:
            # Har funnet startstasjonen og vil da legge til alle delstrekninger frem til sluttstasjonen
            stopp.append(delstrekning)
            if delstrekning[2] == sluttStasjon:
                break
            for index in range(delstrekninger.index(delstrekning)+1, len(delstrekninger)):
                stopp.append(delstrekninger[index])
                if delstrekninger[index][2] == sluttStasjon:
                    break
            break

    # Sjekker at sluttstasjonen inngår i delstrekningene, slik at det ikke bare er startstasjon som inngår i delstrekningene
    # Sjekker listen med stopp er tom
    if len(stopp) == 0 or stopp[-1][2] != sluttStasjon:
        return []

    # Lager en liste med strekningnavnene til alle delstrekningene
    delstrekninger = []
    for delstrekning in stopp:
        delstrekninger.append(delstrekning[6])
    
    return delstrekninger

def updateTicket(con, cursor, ordreNr, plasseringNr, vognNr, ruteID, dato, type, delstrekninger):
    # Oppdaterer billetten med ordrenummeret
    if delstrekninger == []:
        cursor.execute(f"UPDATE Billett SET OrdreNr = ? WHERE {type}Nr = ? AND VognNr = ? AND TogTurID = ? AND TogTurDato = ? AND OrdreNr IS NULL", 
                        (ordreNr, plasseringNr, vognNr, ruteID, dato))
        con.commit()
    else: 
        for delstrekning in delstrekninger:
            cursor.execute(f"""UPDATE Billett SET OrdreNr = ? WHERE {type}Nr = ? AND VognNr = ? 
                                        AND TogTurID = ? AND TogTurDato = ? AND OrdreNr IS NULL AND StrekningNavn = ?""",
                                    (ordreNr, plasseringNr, vognNr, ruteID, dato, delstrekning))
            con.commit()
    return 

# Funksjon som legger til en bestilling i databasen
def orderTickets(con, cursor, plasseringNr, vognNr, ruteID, ordreNr, dato, type, delstrekninger):
    # Sjekker først om plasseringen er ledig på hver delstrekning
    for delstrekning in delstrekninger:
        cursor.execute(f"SELECT OrdreNr From Billett WHERE {type}Nr = ? AND VognNr = ? AND TogTurID = ? AND TogTurDato = ? AND StrekningNavn = ?" , (
            plasseringNr, vognNr, ruteID, dato, delstrekning))
        # Returnerer hvis plasseringen er opptatt
        if cursor.fetchone()[0] != None:
            print("Plasseringen er allerede tatt.")
            return 
        
    # Dersom seng er valgt skal brukeren få velge om man kan ha to senger
    if type == "seng":
        # Finner sengen som er i kupe med denne valgte sengen 
        plasseringNr = int(plasseringNr)
        if plasseringNr % 2 == 0:
            offset = -1
        else:
            offset = 1

        valg = ""
        # Gir valg om å bestille to senger
        while valg != "j" and valg != "n":
            valg = input("Vil du bestille begge sengene i denne kupeen? (j/n): ")
            if valg == "j":
                # Bestiller alle sengene i denne kupeen
                updateTicket(con, cursor, ordreNr, plasseringNr, vognNr, ruteID, dato, type, delstrekninger)
                updateTicket(con, cursor, ordreNr, plasseringNr+offset, vognNr, ruteID, dato, type, delstrekninger)
            elif valg == "n": 
                # Bestiller bare sengen som er valgt
                updateTicket(con, cursor, ordreNr, plasseringNr, vognNr, ruteID, dato, type, delstrekninger)
            else: 
                valg = input("Vennligst skriv inn j eller n: ")
        
        # Setter ordreNr til -1 på alle sengene i kupeen slik at disse er opptatt resten av turen
        updateTicket(con, cursor, -1, plasseringNr, vognNr, ruteID, dato, type, [])
        updateTicket(con, cursor, -1, plasseringNr+offset, vognNr, ruteID, dato, type, [])

    else: 
        # Legger til bestillingen i databasen på hver delstrekning når valgt billett er et sete
        updateTicket(con, cursor, ordreNr, plasseringNr, vognNr, ruteID, dato, type, delstrekninger)
    # Dersom man bestiller en seng, skal denne bli opptatt resten av turen
    print("Bestillingen er lagt til i databasen.")
    return 

# Funksjon som lager en ny kundeordre i databasen og returnerer det nye kundenummeret
def makeOrder(con, cursor, kundeNr):
    dato = datetime.datetime.now().strftime("%Y-%m-%d")
    tidspunkt = datetime.datetime.now().strftime("%H:%M")
    cursor.execute("INSERT INTO KundeOrdre VALUES(NULL, ?, ?, ?)",
                   (tidspunkt, dato, kundeNr))
    con.commit()
    cursor.execute(
        "SELECT OrdreNr FROM KundeOrdre WHERE Dato = ? AND Tidspunkt = ? AND KundeNr = ?", (dato, tidspunkt, kundeNr))
    return cursor.fetchone()[0]

def main():
    con = sqlite3.connect("TogDB_Data.db")
    cursor = con.cursor()

    # Spør brukeren om å logge inn ved å bruke telefonnummeret sitt
    # Lar brukeren prøve på nytt til de logger inn eller skriver "exit"
    tlf = input("Skriv inn telefonnummer (exit for å avslutte): ").strip()
    if tlf == "exit":
        con.close()
        print("Avbrutt")
        return
    while not task_h.login(cursor, tlf):
        tlf = input(
            "Kunne ikke logge inn, prøv igjen (exit for å avslutte): ").strip()
        if tlf.lower() == "exit":
            print("Avbrutt")
            con.close()
            return

    # Henter input fra brukeren
    type = input("Velg en type billett (Seng/Sete) (exit for å avslutte): ").strip().lower()
    while not (type == "seng" or type == "sete"):
        if type == "exit":
            print("Avbrutt")
            con.close()
            return
        type = input("Ugyldig type, velg seng eller sete (exit for å avslutte): ").strip().lower()

    dato = input("Velg dato (YYYY-MM-DD) (exit for å avslutte): ").strip()
    if dato == "exit":
        print("Avbrutt")
        con.close()
        return
    
    startStasjon = input("Velg en startstasjon (exit for å avslutte): ").strip()
    if startStasjon == "exit":
        print("Avbrutt")
        con.close()
        return
    
    sluttStasjon = input("Velg en sluttstasjon (exit for å avslutte): ").strip()
    if sluttStasjon == "exit":
        print("Avbrutt")
        con.close()
        return

    # Henter ut delstrekningene som er en del av ruten fra startStasjon til sluttStasjon
    delstrekninger = getSection(cursor, startStasjon, sluttStasjon, dato)
    # Henter ut ledige billetter basert på input fra brukeren
    billetter = getAvailableTickets(cursor, delstrekninger, dato, type)

    # Lager liste med gyldige verdier for ruter, vogn og plassering  
    gyldigeVerdier = dict()

    # Presenterer resultatet
    print("Resultat:")
    if len(billetter) == 0 or len(billetter[0]) == 0:
        print("Ingen tilgjengelige billetter.")
        con.close()
        return
    else:
        for i in range(len(billetter[0])):
            ruteID = billetter[0][i][1]
            vognNr = billetter[0][i][2]
            seteNr = billetter[0][i][3]
            sengNr = billetter[0][i][4]

            if gyldigeVerdier.get(ruteID) == None:
                if type == "sete":
                    gyldigeVerdier[ruteID] = [(vognNr, seteNr)]
                elif type == "seng":
                    gyldigeVerdier[ruteID] = [(vognNr, sengNr)]
            else:
                if type == "sete":
                    gyldigeVerdier[ruteID].append((vognNr, seteNr))
                elif type == "seng":
                    gyldigeVerdier[ruteID].append((vognNr, sengNr))

            avgangstid = billetter[0][i][8]
            ankomsttid = billetter[-1][i][9]
            startStasjon = billetter[0][i][10]
            sluttStasjon = billetter[-1][i][11]
            if type == "sete":
                print(
                    f"Rute {ruteID}: {startStasjon} - {sluttStasjon} (Vogn {vognNr}, sete {seteNr}): {avgangstid} - {ankomsttid}")
            elif type == "seng":
                print(
                    f"Rute {ruteID}: {startStasjon} - {sluttStasjon} (Vogn {vognNr}, seng {sengNr}): {avgangstid} - {ankomsttid}")
            else:
                print("Ikke gyldig billettype.")
                con.close()
                return
        print("\n")

    # Lager en kundeordre og returnerer ordrenummeret
    cursor.execute("SELECT KundeNr FROM Kunde WHERE TelefonNr = ?", (tlf,))
    kundeNr = cursor.fetchone()[0]
    ordreNr = makeOrder(con, cursor, kundeNr)
    # Henter ut ruteID, vognNr og plasseringNr fra brukeren for å bestille billett
    ruteID = input("Velg ruteID: ").strip()
    vognNr = input("Velg vognNr: ").strip()
    plasseringNr = input(f"Velg {type}Nr: ").strip()

     # Passer på at brukeren skriver inn gyldige verdier
    while True:
        if int(ruteID) not in gyldigeVerdier.keys() or gyldigeVerdier.get(ruteID, (vognNr, plasseringNr)) != (vognNr, plasseringNr):
            print("\nUgyldige verdier, prøv igjen.")
            ruteID = input("Velg ruteID: ").strip() 
            vognNr = input("Velg vognNr: ").strip()
            plasseringNr = input(f"Velg {type}: ").strip()
        else:
            break

    # Bestiller billett avhengig av typen billett
    if type == "sete":
        orderTickets(con, cursor, plasseringNr, vognNr,
                    ruteID, ordreNr, dato, type, delstrekninger)
    elif type == "seng":
        orderTickets(con, cursor, plasseringNr, vognNr,
                    ruteID, ordreNr, dato, type, delstrekninger)
    
    con.close()

