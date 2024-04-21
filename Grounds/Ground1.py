import random
import pygame
from Elements.Portal import Portale
from Elements.Cristal import Cristallo
from Elements.Blocco import Blocco, BloccoSpecial
from SpecialElements.accellerator import Accelerator


class Terreno1:
    def __init__(self, gioco, colore_obbligatorio, colore_iniziale=None):
        self.contatore_accellerators_generati = 0
        self.funzione_verifica_accelerazione = lambda: None
        self.chiamata_per_cristallo_obbligatorio = random.randint(1, 5)
        self.cristallo_colore_obbligatorio_generato = False
        self.contatore_cristalli_generati = 0
        self.gioco = gioco
        self.porzioni = []
        self.cristalli = pygame.sprite.Group()
        self.accellerators = pygame.sprite.Group()
        self.ultima_altezza = self.gioco.ALTEZZA - 50
        self.portale_inizio = None  # Inizializzaz
        # ione qui, ma assegnazione nel metodo genera_terreno_iniziale
        self.portale_fine = None
        self.colore_obbligatorio = colore_obbligatorio
        self.colore_iniziale = colore_iniziale
        self.rainbow_locale = list(Cristallo.RAINBOW)
        self.COLORE_LAVA = Cristallo.RAINBOW[1]
        self.num_blocco = random.randint(16, 30)
        self.max_salto = gioco.SALTO_MAX
        self.limite_blocco_lava = self.num_blocco - 1
        self.num_blocco_lava = 0
        self.limite_blocco_lava = random.randint(3, 6)
        self.velocita = self.gioco.VELOCITA_TERRENO
        self.rainbow_locale.remove(colore_obbligatorio)
        self.sfondo_lava_img = pygame.image.load(
            "C:/Users/gvmaz/OneDrive/Desktop/IA/Progetti/Infinity_alpha/Immagini/lava2.jpg").convert()
        self.sfondo_lava1_x = 0  # Posizione iniziale della prima copia
        self.sfondo_lava_imgs_x = [0, self.sfondo_lava_img.get_width(), 2 * self.sfondo_lava_img.get_width(),
                                   3 * self.sfondo_lava_img.get_width()]
        self.accelerazione()
        self.accellerator_on = False
        self.genera_terreno_iniziale()

    def genera_terreno_iniziale(self):
        x_pos = 0

        # Creazione e aggiunta del blocco iniziale
        larghezza_blocco_iniziale = 200
        blocco_iniziale = Blocco(x_pos, self.ultima_altezza - 50, larghezza_blocco_iniziale, 50, self.gioco.GROUND1)
        self.porzioni.append(blocco_iniziale)

        # Creazione e posizionamento del portale di inizio sopra il blocco iniziale
        self.portale_inizio = Portale(self.gioco, x_pos + larghezza_blocco_iniziale / 2, self.ultima_altezza - 125,
                                      self.colore_iniziale if self.colore_iniziale else self.gioco.NEXT_COLOR)

        x_pos += larghezza_blocco_iniziale

        # Ciclo per generare blocchi e blocchi lava alternati
        alterna = True
        for _ in range(self.num_blocco - 1):
            if alterna:
                # Genera e aggiungi Blocco
                larghezza_blocco = random.randint(550, 850)
                blocco = Blocco(x_pos, self.ultima_altezza - 50, larghezza_blocco, 50, self.gioco.GROUND1)
                self.genera_cristallo_per_porzione(blocco)
                self.genera_accellerator_per_porzione(blocco)
            else:
                # Genera e aggiungi BloccoLava
                counter = random.randint(1,5)
                if counter == 2 or counter == 4:
                    larghezza_blocco = random.randint(500, 1000)

                    blocco = BloccoSpecial(x_pos, self.ultima_altezza - 50, larghezza_blocco, 50)
                else:
                    larghezza_blocco = random.randint(200, 400)
                    blocco = BloccoSpecial(x_pos, self.ultima_altezza - 50, larghezza_blocco, 50)
            self.porzioni.append(blocco)
            x_pos += larghezza_blocco
            alterna = not alterna

        # Genera il blocco finale con il portale di fine
        larghezza_blocco_finale = 200
        blocco_finale = Blocco(x_pos, self.ultima_altezza - 50, larghezza_blocco_finale, 50, self.gioco.GROUND1)
        self.porzioni.append(blocco_finale)
        self.portale_fine = Portale(self.gioco, x_pos + larghezza_blocco_finale / 2, self.ultima_altezza - 125,
                                    self.colore_obbligatorio)
        # print(self.porzioni)

    def aggiorna(self):

        for porzione in self.porzioni:
            porzione.rect.x += self.velocita

        for cristallo in self.cristalli:
            cristallo.rect.x += self.velocita

        for accellerator in self.accellerators:
            accellerator.rect.x += self.velocita

        if self.portale_inizio:
            self.portale_inizio.rect.x += self.velocita
        if self.portale_fine:
            self.portale_fine.rect.x += self.velocita

            # Aggiorna la posizione dello sfondo della lava
            self.sfondo_lava_imgs_x = [x + self.velocita for x in self.sfondo_lava_imgs_x]

            # Riorganizza lo sfondo per creare un effetto di scorrimento continuo
            for i, x in enumerate(self.sfondo_lava_imgs_x):
                if x + self.sfondo_lava_img.get_width() < 0:
                    self.sfondo_lava_imgs_x[i] += 4 * self.sfondo_lava_img.get_width()

    def disegna(self, superficie):
        for x in self.sfondo_lava_imgs_x:
            superficie.blit(self.sfondo_lava_img, (x, self.ultima_altezza))
        # Ora disegna le porzioni del terreno e gli altri elementi sopra lo sfondo arancione
        for porzione in self.porzioni:
            porzione.disegna(superficie)
        for cristallo in self.cristalli:
            cristallo.disegna(superficie)
        for accellerator in self.accellerators:
            accellerator.disegna(superficie)
        if self.portale_inizio:
            self.portale_inizio.disegna(superficie)
        if self.portale_fine:
            self.portale_fine.disegna(superficie)

    def genera_cristallo_per_porzione(self, porzione):
        if self.portale_fine and porzione == self.porzioni[-1]:
            # Non generare cristalli su questa porzione se è destinata al portale di fine
            return

        self.contatore_cristalli_generati += 1

        centro_porzione = (porzione.left + porzione.right) / 2
        larghezza_centrale_vietata = 100
        margine = 20  # Margine dai bordi laterali della porzione

        # Calcolare gli intervalli laterali escludendo l'area centrale di 80 unità
        intervallo_sx = (porzione.left + margine, centro_porzione - larghezza_centrale_vietata / 2)
        intervallo_dx = (centro_porzione + larghezza_centrale_vietata / 2, porzione.right - margine)

        # Scegliere randomicamente da quale intervallo selezionare x
        if random.choice([True, False]):
            x = random.randrange(int(intervallo_sx[0]), int(intervallo_sx[1]))
        else:
            x = random.randrange(int(intervallo_dx[0]), int(intervallo_dx[1]))

        y = porzione.top - 60

        if not self.cristallo_colore_obbligatorio_generato and self.contatore_cristalli_generati == self.chiamata_per_cristallo_obbligatorio:
            cristallo = Cristallo(x, y, self.colore_obbligatorio)
            self.cristallo_colore_obbligatorio_generato = True
        else:
            colore_random = random.choice(self.rainbow_locale)  # Usa la copia locale per scegliere un colore casuale
            cristallo = Cristallo(x, y, colore_random)

        self.cristalli.add(cristallo)

    def genera_accellerator_per_porzione(self, porzione):
        if self.portale_fine and porzione == self.porzioni[-1]:
            # Non generare accelleratori su questa porzione se è destinata al portale di fine
            return

        centro_x_porzione = porzione.left + porzione.larghezza / 2
        larghezza_accellerator = 50
        x = centro_x_porzione - larghezza_accellerator / 2  # Posiziona l'x in modo che l'Accelerator sia centrato
        y = porzione.top - 60  # Questo già posiziona l'Accelerator sopra la porzione

        # Assicurati che il costruttore di Accelerator accetti tutti i parametri necessari
        # Potrebbe essere necessario passare ulteriori parametri oltre a x e y, a seconda della tua implementazione
        accellerator = Accelerator(x, y)
        self.accellerators.add(accellerator)

    def accelerazione(self):
        tempo_inizio = pygame.time.get_ticks()  # Memorizza il momento in cui l'accelerazione inizia
        durata_accelerazione = 5000  # Durata dell'accelerazione in millisecondi (5 secondi)
        velocità_originale = self.velocita
        self.accellerator_on = True
        self.velocita += -5  # Aumenta la velocità

        # Definisci una funzione interna per verificare se l'effetto di accelerazione è ancora attivo
        def verifica_accelerazione():
            tempo_attuale = pygame.time.get_ticks()
            if tempo_attuale - tempo_inizio > durata_accelerazione:
                self.velocita = velocità_originale  # Ripristina la velocità al suo valore originale
                self.accellerator_on = False
        # Memorizza la funzione di verifica per poterla chiamare ogni frame nel ciclo di gioco principale
        self.funzione_verifica_accelerazione = verifica_accelerazione
