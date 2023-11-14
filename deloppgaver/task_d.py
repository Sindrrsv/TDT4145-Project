import datetime
import sqlite3
import deloppgaver.task_g as task_g

# Funksjon som returnerer alle togturene som går mellom to stasjoner på en gitt dag og tidspunkt
def getTogruter(cursor, startstasjon, sluttstasjon, dato, tidspunkt):
    # Finner neste dato
    nesteDato = datetime.datetime.strptime(dato, "%Y-%m-%d") + datetime.timedelta(days=1)
    nesteDato = nesteDato.date()

    # Finner ut om ruten går mot eller med hovedretningen 
    retning = task_g.getDirection(startstasjon, sluttstasjon)

    # Hvis det ikke går en rute mellom stasjonene, returner en tom liste
    if retning == []:
        return []

    # Sjekke om det går en direkte delstrekning mellom stasjonene 
    cursor.execute("""SELECT * FROM Delstrekning WHERE StartStasjon = ? AND SluttStasjon = ?""", (startstasjon, sluttstasjon))
    strekning = cursor.fetchall()
    
    # Dersom det går en direkte delstrekning mellom stasjonene, returner alle togturene som går mellom stasjonene på den dagen
    if len(strekning) != 0:
        cursor.execute("""SELECT RuteID, Navn, Startstasjon, Sluttstasjon, OperatoerNavn, Dato,  AvgangsTid, AnkomstTid FROM Togrute
        JOIN Togtur USING (RuteID)
        JOIN KjoererDelstrekning USING (RuteID)
        JOIN Delstrekning USING (StrekningNavn)
        WHERE (StartStasjon = ? AND SluttStasjon = ?) AND ((Dato = ? AND AvgangsTid >= ?) OR Dato = ?)
        ORDER BY Dato, AvgangsTid""", (startstasjon, sluttstasjon, dato, tidspunkt, nesteDato))

    # Dersom det ikke går en direkte delstrekning mellom stasjonene, returner alle togturene som går mellom de to stasjonene på den dagen
    # Disse vil alltid få to resultater fra spørringen, en for startstasjonen og en for sluttstasjonen,
    # og vi kan derfor bruke GROUP BY og HAVING for å filtrere ut de som ikke har to resultater
    else: 
        cursor.execute(f"""SELECT RuteID, Navn, Startstasjon, Sluttstasjon, OperatoerNavn, Dato,  AvgangsTid, AnkomstTid FROM Togrute
        JOIN Togtur USING (RuteID) 
        JOIN KjoererDelstrekning USING (RuteID) 
        JOIN Delstrekning USING (StrekningNavn)
        WHERE (StartStasjon = ? OR SluttStasjon = ?) AND ((Dato = ? AND AvgangsTid >= ?) OR Dato = ?) AND {retning} IS NULL
        GROUP BY RuteID, Dato HAVING COUNT(*) = 2
        ORDER BY Dato, AvgangsTid""", 
        (startstasjon, sluttstasjon, dato, tidspunkt, nesteDato))
    return cursor.fetchall()

def main(): 
    print("Dette vil søke etter ruter som går mellom to stasjoner på en gitt dag og tidspunkt.")
    con = sqlite3.connect("TogDB_Data.db")
    cursor = con.cursor()
    
    # Henter ut data fra brukeren 
    startstasjon = input("Velg startstasjon: ").strip()
    sluttstasjon = input("Velg endestasjon: ").strip()
    dato = input("Velg en dato (YYYY-MM-DD): ").strip()
    tidspunkt = input("Velg tidspunkt (HH:MM): ").strip()
    ruter = getTogruter(cursor, startstasjon, sluttstasjon, dato, tidspunkt)

    # Hvis det ikke er noen ruter tilgjengelig, informer brukeren om dette
    if len(ruter) == 0:
        print("Fant ingen ruter.")

    # Hvis det er ruter tilgjengelig, skriv ut informasjon om disse på en ryddig måte
    for rute in ruter:
        ruteID = rute[0]
        navn = rute[1]
        startstasjon = rute[2]
        sluttstasjon = rute[3]
        operatoerNavn = rute[4]
        dato = rute[5]
        avgangstid = rute[6]
        print(f"Rute {ruteID} ({navn}) fra {startstasjon} til {sluttstasjon} kjøres av {operatoerNavn} på {dato} med avgangstid {avgangstid}")

    con.close() 
