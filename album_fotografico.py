from csv import DictReader



def carica_da_file(nomeFile, album):
    """Carica le foto dal file, creando un nuovo anno ogni volta che compare per la prima volta"""

    try:
        file = open(nomeFile, "r")
        reader = DictReader(file, skipinitialspace=True) #skipinitialspace elimina lo spazio all'inizio delle chiavi e
                                                         #impedisce la generazione di eventuali errori successivi dovuti al confronto tra chiavi
        for foto in reader:
            album.append(foto)

        file.close()
        return album


    except FileNotFoundError:
        return None



def aggiungi_foto(album, codice, titolo, autore, mese, anno, file_path):
    """Aggiunge una foto all'album, creando l'anno al volo se non è ancora presente"""
    for foto in album:
        if foto["codice"].upper() == codice.upper(): #controlla che non esistono codici già presenti, data la loro univocità
            print("Codice già presente!")
            return False

    newFoto = {
        "codice": codice,
        "titolo": titolo,
        "autore": autore,
        "mese": str(mese),
        "anno": str(anno),
        }

    album.append(newFoto)

    fileout = open(file_path, "a")
    fileout.write(",".join(list(newFoto.values())) + "\n") #aggiugo al file la foto appena creata separando i campi con la virgola
    fileout.close()                                  #il join mi serve per mettere in una stringa gli elementi della lista ricavata da newFoto


    return True

def cerca_foto(album, codice):
    """Cerca una foto nell'album dato il codice"""
    trovato = False
    i = 0
    for foto in album:
        if codice.upper() == foto["codice"].upper():
            trovato = True
            break
        else:
            i += 1
    return trovato, i


def elenco_foto_anno_per_titolo(album, anno):
    """Ordina i titoli delle foto di un dato anno in ordine alfabetico"""
    listaAnno = []
    for foto in album:
        if foto["anno"] == str(anno):
            listaAnno.append(foto["titolo"])
    listaAnno.sort()

    if listaAnno == []:
        return None

    return listaAnno

def main():
    album = []
    file_path = "album_fotografico.csv"

    while True:
        print("\n--- MENU ALBUM FOTOGRAFICO ---")
        print("1. Carica album da file")
        print("2. Aggiungi una nuova foto")
        print("3. Cerca una foto per codice")
        print("4. Elenco foto di un anno (ordinato per titolo)")
        print("5. Esci")

        scelta = input("Scegli un'opzione >> ").strip()

        if scelta == "1":
            file_path = input("Inserisci il path del file da caricare: ").strip()  # nelle funzioni è "nomeFile"
            while True:
                prova = carica_da_file(file_path, album)
                if prova is not None:
                    album = prova       #permetto al programma di non bloccarsi qualora il file non fosse stato trovato...
                    break
                else:
                    file_path = input("File non trovato. Reinserisci il path del file da caricare: ").strip()
                    #...e di richiedere nuovamente il path
            print(album)

        elif scelta == "2":
            if not album:
                print("Prima carica l'album da file.")
                continue

            codice = input("Codice della foto: ").strip()
            titolo = input("Titolo: ").strip()
            autore = input("Autore: ").strip()
            try:
                valido = False
                while not valido:
                    mese = int(input("Mese (1-12): ").strip())
                    if mese < 1 or mese > 12:
                        print("il mese inserito non è valido. riprova")
                    else:
                        valido = True
                anno = int(input("Anno: ").strip())

            except ValueError:
                print("Errore: inserire valori numerici validi per mese e anno.")
                continue

            foto = aggiungi_foto(album, codice, titolo, autore, mese, anno, file_path)
            if foto:
                print(f"Foto aggiunta con successo!")
                print(", ".join(list(album[-1].values())))
            else:
                print("Non è stato possibile aggiungere la foto.")

        elif scelta == "3":
            if not album:
                print("L'album è vuoto.")
                continue

            codice = input("Inserisci il codice della foto da cercare: ").strip()
            risultato, indice = cerca_foto(album, codice)
            if risultato:
                print(f"Foto trovata:")
                print(", ".join(list(album[indice].values())))
            else:
                print("Foto non trovata.")

        elif scelta == "4":
            if not album:
                print("L'album è vuoto.")
                continue

            try:
                anno = int(input("Inserisci l'anno da consultare: ").strip())
            except ValueError:
                print("Errore: inserire un valore numerico valido.")
                continue

            titoli = elenco_foto_anno_per_titolo(album, anno)
            if titoli is not None:
                print(f'\nFoto del {anno}:')
                print("\n".join([f"- {titolo}" for titolo in titoli]))
            else:
                print(f"Nessuna foto trovata per l'anno {anno}.")

        elif scelta == "5":
            print("Uscita dal programma...")
            break
        else:
            print("Opzione non valida. Riprova.")


if __name__ == "__main__":
    main()
