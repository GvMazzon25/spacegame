import re


class Configurazione:
    def __init__(self):
        self.image = ''
        self.sfondo = ()
        self.skin = ()
        self.ground = ()
        self.main_color = ()
        self.secondary_color = ()
        self.color_default = ()
        self.speed_ground = 0
        self.min_distance = 0
        self.max_distance = 0
        self.max_height = 0
        self.max_jump = 0
        self.black = (0, 0, 0)
        self.red = (255, 0, 0)  # Rosso
        self.orange = (255, 165, 0)  # Arancione
        self.yellow = (255, 255, 0)  # Giallo
        self.green = (0, 128, 0)  # Verde
        self.blue = (0, 0, 255)  # Blu
        self.indigo = (75, 0, 130)  # Indaco
        self.violet = (238, 130, 238)  # Violetto
        self.white = (255, 255, 255)  # Bianco
        self.mode = ""
        self.score = 0
        self.rainbow = []
        self.images = []
        self.dataset = 'C:/Users/gvmaz/OneDrive/Desktop/IA/Progetti/Infinity_alpha/Utility/dataset.txt'
        self.configurazioni = []
        self.index = 0

    def ottieni_configurazione(self, numero):
        if 0 <= numero < len(self.configurazioni):
            return self.configurazioni[numero]
        else:
            raise IndexError("Numero di configurazione non valido.")

    def crea_lista_colori(self):
        # Creazione della lista di colori
        lista_colori = [
            self.black,
            self.red,
            self.orange,
            self.yellow,
            self.green,
            self.blue,
            self.indigo,
            self.violet,
            self.white
        ]
        self.rainbow = lista_colori
        return self.rainbow

    def select_image(self, n):
        # Creazione della lista di link alle immagini
        lista_image = [
            'C:/Users/gvmaz/OneDrive/Desktop/IA/Progetti/Infinity_alpha/Immagini/black.jpg',
            'C:/Users/gvmaz/OneDrive/Desktop/IA/Progetti/Infinity_alpha/Immagini/red.jpg',
            'C:/Users/gvmaz/OneDrive/Desktop/IA/Progetti/Infinity_alpha/Immagini/orange.jpg',
            'C:/Users/gvmaz/OneDrive/Desktop/IA/Progetti/Infinity_alpha/Immagini/yellow.jpg',
            'C:/Users/gvmaz/OneDrive/Desktop/IA/Progetti/Infinity_alpha/Immagini/green.jpg',
            'C:/Users/gvmaz/OneDrive/Desktop/IA/Progetti/Infinity_alpha/Immagini/blue.jpg',
            'C:/Users/gvmaz/OneDrive/Desktop/IA/Progetti/Infinity_alpha/Immagini/indigo.jpg',
            'C:/Users/gvmaz/OneDrive/Desktop/IA/Progetti/Infinity_alpha/Immagini/violet.jpg',
            'C:/Users/gvmaz/OneDrive/Desktop/IA/Progetti/Infinity_alpha/Immagini/white.jpg'
        ]
        self.images = lista_image
        return self.images[n]

    def crea_struttura(self, main_color, previus_color, current_color, mode):
        # Assegnazione dei valori specifici
        self.sfondo = current_color
        self.skin = self.blue
        self.ground = self.sfondo
        self.main_color = main_color

        # Assegnazione dei valori per le "Rules"
        if self.index == 0:
            self.speed_ground = -6
        else:
            self.speed_ground = -8
        self.min_distance = 150
        self.max_distance = 300
        self.max_height = 50
        self.max_jump = 100
        self.mode = mode

        # Assegnazione dell'immagine corrispondente all'indice attuale
        image_path = self.select_image(self.index)

        # Creazione delle strutture dati
        data = {
            'Image': image_path,
            'Palette': {
                'SFONDO': self.sfondo,
                'SKIN': previus_color,
                'TERRENO': self.ground,
                'ROSSO': self.red,
                'NEXT_COLOR': previus_color,
                'MAIN_COLOR': self.main_color,
            },
            'Rules': {
                'MODE': self.mode,
                'VELOCITA_TERRENO': self.speed_ground,
                'DISTANZA_ORIZZONTALE_MIN': self.min_distance,
                'DISTANZA_ORIZZONTALE_MAX': self.max_distance,
                'DIFFERENZA_ALTEZZA_MAX': self.max_height,
                'SALTO_MAX': self.max_jump,
            }
        }

        # Incremento dell'indice per la prossima chiamata
        self.index += 1

        return data

    def genera_lista_strutture(self):
        lista = self.crea_lista_colori()
        mode = self.leggi_modality()
        # Assicurati che la lista abbia un numero sufficiente di elementi
        if len(lista) < 2:
            raise ValueError("La lista deve contenere almeno due elementi")

        # Crea la lista di strutture ciclando sulla lista di colori
        lista_strutture = [
            self.crea_struttura(lista[(i + 1) % len(lista)], lista[(i - 1) % len(lista)], lista[i], mode)
            for i in range(len(lista))
        ]
        self.configurazioni = lista_strutture
        self.index = 0
        return self.configurazioni

    # Score
    def replace_score(self, nuovo_numero):
        file_path = self.dataset
        linee_modificate = []

        with open(file_path, 'r') as file:
            for linea in file:
                # Controlla se la linea contiene la parola "Score"
                if "Score" in linea:
                    # Usa una funzione di callback per verificare e sostituire il numero
                    def sostituisci(match):
                        numero_attuale = int(match.group(2))  # Estrai il numero attuale
                        if nuovo_numero > numero_attuale:
                            return f"{match.group(1)}{nuovo_numero}"  # Sostituisce se nuovo_numero è maggiore
                        else:
                            return match.group(0)  # Altrimenti, lascia inalterato

                    linea_modificata = re.sub(r'(Max-Score: )(\d+)', sostituisci, linea)
                    linee_modificate.append(linea_modificata)
                else:
                    linee_modificate.append(linea)

        # Sovrascrive il file con le linee modificate
        with open(file_path, 'w') as file:
            file.writelines(linee_modificate)

        print("Modifica completata!")

    def reset_score(self):
        linee_modificate = []

        with open(self.dataset, 'r') as file:
            for linea in file:
                # Cerca la linea che contiene "Score:" e sostituisce il numero successivo con 0
                # Utilizziamo una funzione lambda per la sostituzione
                linea_modificata = re.sub(r'(Max-Score: )\d+', lambda match: match.group(1) + str(0), linea)
                linee_modificate.append(linea_modificata)

        # Sovrascrive il file con le linee modificate per azzerare lo score
        with open(self.dataset, 'w') as file:
            file.writelines(linee_modificate)

        print("Score azzerato a 0.")

    # Level Passed
    def leggi_level_passed(self):
        file_path = self.dataset
        livello_corrente = 0  # Default value in case "Level_Passed:" is not found

        with open(file_path, 'r') as file:
            for linea in file:
                if linea.startswith("Level_Passed:"):
                    # Split the line at ": " and take the second part as the level passed.
                    # Also, strip() is used to remove any leading/trailing whitespace and newlines.
                    livello_corrente = int(linea.split(": ")[1].strip())  # Convert to integer
                    break  # Exit the loop once "Level_Passed:" is found

        print(f"Il livello corrente è: {livello_corrente}")
        return livello_corrente

    def replace_level_passed(self, nuovo_valore):
        file_path = self.dataset
        linee_modificate = []

        with open(file_path, 'r') as file:
            for linea in file:
                # Controlla se la linea contiene la parola "Level_Passed"
                if "Level_Passed" in linea:
                    # Usa una funzione di callback per verificare e sostituire il numero
                    def sostituisci(match):
                        valore_attuale = int(match.group(2))  # Estrai il valore attuale
                        if nuovo_valore > valore_attuale:
                            return f"{match.group(1)}{nuovo_valore}"  # Sostituisce se nuovo_valore è maggiore
                        else:
                            return match.group(0)  # Altrimenti, lascia inalterato

                    linea_modificata = re.sub(r'(Level_Passed: )(\d+)', sostituisci, linea)
                    linee_modificate.append(linea_modificata)
                else:
                    linee_modificate.append(linea)

        # Sovrascrive il file con le linee modificate
        with open(file_path, 'w') as file:
            file.writelines(linee_modificate)

        print("Modifica completata!")

    def reset_level_passed(self):
        linee_modificate = []

        with open(self.dataset, 'r') as file:
            for linea in file:
                # Cerca la linea che contiene "Score:" e sostituisce il numero successivo con 0
                # Utilizziamo una funzione lambda per la sostituzione
                linea_modificata = re.sub(r'(Level_Passed: )\d+', lambda match: match.group(1) + str(0), linea)
                linee_modificate.append(linea_modificata)

        # Sovrascrive il file con le linee modificate per azzerare lo score
        with open(self.dataset, 'w') as file:
            file.writelines(linee_modificate)

        print("Score azzerato a 0.")

    # Modalità
    def leggi_modality(self):
        file_path = self.dataset
        modalita_corrente = "Nessuna"  # Default value in case "Modality:" is not found

        with open(file_path, 'r') as file:
            for linea in file:
                if linea.startswith("Modality:"):
                    # Split the line at ": " and take the second part as the current mode.
                    # Also, strip() is used to remove any leading/trailing whitespace and newlines.
                    modalita_corrente = linea.split(": ")[1].strip()
                    break  # Exit the loop once "Modality:" is found

        print(f"La modalità corrente è: {modalita_corrente}")
        return modalita_corrente

    def modifica_modality(self, nuova_modalita):
        file_path = self.dataset
        linee_modificate = []

        with open(file_path, 'r') as file:
            for linea in file:
                if linea.startswith("Modality:"):
                    linea_modificata = f"Modality: {nuova_modalita}\n"
                    linee_modificate.append(linea_modificata)
                else:
                    linee_modificate.append(linea)

        with open(file_path, 'w') as file:
            file.writelines(linee_modificate)

        print("Modality modificata.")

    def reset_modality(self):
        file_path = self.dataset
        linee_modificate = []

        with open(file_path, 'r') as file:
            for linea in file:
                if linea.startswith("Modality:"):
                    linea_modificata = "Modality: Nessuna\n"
                    linee_modificate.append(linea_modificata)
                else:
                    linee_modificate.append(linea)

        with open(file_path, 'w') as file:
            file.writelines(linee_modificate)

        print("Modality resettata a 'Nessuna'.")


if __name__ == "__main__":
    gioco = Configurazione()
    list = gioco.genera_lista_strutture()
    print(list)
