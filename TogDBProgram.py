# Importerer funksjonene vi lagde i andre deloppgaver
import deloppgaver.task_c as task_c
import deloppgaver.task_d as task_d
import deloppgaver.task_e as task_e
import deloppgaver.task_g as task_g
import deloppgaver.task_h as task_h

def main(): 
    # Initialiserer databasen og henter ut tilkobling og cursor
    print("Velkommen til TogDB-programmet!")
    print("Programmet bruker 'oe' istedenfor 'ø', 'ae' istedenfor 'æ' og 'aa' istedenfor 'å'.")
    print("Dette gjelder alle inputs.")

    # Loop som kjører frem til brukeren velger å avlsuttet programmet
    while True:
        print("\nVelg et alternativ: \n1: Søk etter ruter på en gitt dag \n2: Søk etter ruter mellom to stasjoner på en gitt dag \n3: Registrer kunde \n4: Bestill billetter \n5: Vis dine fremtidige ordrer \n0: Avslutt")
        valg = input("> ").strip()

        # Brukeren velger å søke etter ruter på en stasjon på en dag, dette vil bruke funskjonen fra task_c
        if valg == "1":
            task_c.main()

        # Brukeren velger å søke etter ruter mellom to stasjoner på en dag, dette vil bruke funksjonen fra task_d
        elif valg == "2":
            task_d.main()

        # Brukeren velger å registrere en kunde, dette vil bruke funksjonen fra task_e
        elif valg == "3":
            task_e.main()
        
        # Brukeren velger å bestille billetter, dette vil bruke funksjonen fra task_g
        elif valg == "4": 
           task_g.main()

        # Brukeren velger å hente ut fremtidge bestillte billetter, dette vil bruke funksjonen fra task_h
        elif valg == "5": 
            task_h.main()

        # Brukeren velger å avlsutte programmet
        elif valg == "0":
            break
        
        # Brukeren skriver inn noe annet enn tall 0 til 5 
        else:
            print("Ugyldig input, prøv igjen.")

main()
