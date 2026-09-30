from csv import DictReader
from pprint import pprint


def carica_da_file(nomeFile, album):
    """Carica le foto dal file, creando un nuovo anno ogni volta che compare per la prima volta"""

    try:
        file = open(nomeFile, "r")
        reader = DictReader(file, skipinitialspace=True)

        for foto in reader:
            album.append(foto)

        file.close()
        return album


    except FileNotFoundError:
        return None



def aggiungi_foto(album, codice, titolo, autore, mese, anno, file_path):
    """Aggiunge una foto all'album, creando l'anno al volo se non è ancora presente"""
    for foto in album:
        if foto["codice"].upper() == codice.upper() or foto["titolo"].upper() == titolo.upper():
            print("Codice e/o titolo già presente!")
            return False

    newFoto = {
        "codice": codice,
        "titolo": titolo,
        "autore": autore,
        "mese": str(mese),
        "anno": str(anno),
        }

    album.append(newFoto)

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
    # TODO


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
            while True:
                file_path = input("Inserisci il path del file da caricare: ").strip() #nelle funzioni è "nomeFile"
                prova = carica_da_file(file_path, album)
                if prova is not None:
                    album = prova
                    break
            pprint(album)

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
                pprint(album)
            else:
                print("Non è stato possibile aggiungere la foto.")

        elif scelta == "3":
            if not album:
                print("L'album è vuoto.")
                continue

            codice = input("Inserisci il codice della foto da cercare: ").strip()
            risultato, indice = cerca_foto(album, codice)
            if risultato:
                print(f"Foto trovata:\n{album[indice]}")
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
