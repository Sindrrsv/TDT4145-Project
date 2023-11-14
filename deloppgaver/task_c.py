import sqlite3

# Denne funksjonen vil returnere en liste med alle ruter som går fra eller til en gitt stasjon på en gitt dag.
# Funksjonen kjoerer en SQL spoerring som henter ut ruteID, operatoernavn og dag fra tabellen Togrute, Dager og KjoererDelstrekning.
def getTogruterStasjon(cursor, stasjon, dag):
    cursor.execute("""SELECT DISTINCT RuteID, Navn, OperatoerNavn FROM Togrute
    JOIN Dager USING (RuteID) 
    JOIN KjoererDelstrekning USING (RuteID) 
    JOIN Delstrekning USING (StrekningNavn)
    WHERE (StartStasjon = ? OR SluttStasjon = ?) AND Dag = ?""", (stasjon, stasjon, dag))
    return cursor.fetchall()

def main(): 
    print("Dette vil søke etter ruter som går fra eller til en gitt stasjon på en gitt dag.")
    # Henter input fra bruker 
    stasjon = input("Skriv inn en stasjon: ").strip()
    dag = input("Skriv inn en ukedag: ").strip()
    con = sqlite3.connect("TogDB_Data.db")
    cursor = con.cursor()

    # Henter rutene basert på input 
    togruter = getTogruterStasjon(cursor, stasjon, dag)

    # Presenterer resultatet av søket på en ryddig måte
    print("Resultater:")
    if togruter == []:
        print("Ingen ruter funnet.")
    for togrute in togruter:
        ruteID = togrute[0]
        ruteNavn = togrute[1]
        operatoerNavn = togrute[2]
        print(f"Rute {ruteID} ({ruteNavn}) kjøres av {operatoerNavn} på {dag}.")

    con.close()

