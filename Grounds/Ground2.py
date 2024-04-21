import random
import pygame
from Elements.Portal import Portale
from Elements.Cristal import Cristallo
from Elements.Blocco import Blocco, BloccoSand
from SpecialElements.Worm import Worm


class Terreno2:
    def __init__(self, gioco, colore_obbligatorio, colore_iniziale=None):
        self.porzione = None
        self.worm = Worm
        self.worms = pygame.sprite.Group()
        self.contatore_worm = 0
        self.funzione_verifica_accelerazione = lambda: None
        self.chiamata_per_cristallo_obbligatorio = random.randint(1, 5)
        self.cristallo_colore_obbligatorio_generato = False
        self.contatore_cristalli_generati = 0
        self.gioco = gioco
        self.porzioni = []
        self.cristalli = pygame.sprite.Group()
        self.ultima_altezza = self.gioco.ALTEZZA - 50
        self.portale_inizio = None  # Inizializzaz
        self.portale_fine = None
        self.colore_obbligatorio = colore_obbligatorio
        self.colore_iniziale = colore_iniziale
        self.rainbow_locale = list(Cristallo.RAINBOW)
        self.num_blocco = random.randint(16, 30)
        self.max_salto = gioco.SALTO_MAX
        self.velocita = self.gioco.VELOCITA_TERRENO
        self.rainbow_locale.remove(colore_obbligatorio)
        self.genera_terreno_iniziale()

    def genera_terreno_iniziale(self):
        x_pos = 0

        # Creazione e aggiunta del blocco iniziale
        larghezza_blocco_iniziale = 200
        blocco_iniziale = Blocco(x_pos, self.ultima_altezza, larghezza_blocco_iniziale, 50, self.gioco.GROUND1)
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
                blocco = Blocco(x_pos, self.ultima_altezza, larghezza_blocco, 50, self.gioco.GROUND1)
                self.genera_cristallo_per_porzione(blocco)
                self.genera_worm_per_porzione(blocco)
            else:
                larghezza_blocco = random.randint(300, 450)
                blocco = BloccoSand(x_pos, self.ultima_altezza, larghezza_blocco, 50)

            self.porzioni.append(blocco)
            x_pos += larghezza_blocco
            alterna = not alterna

        # Genera il blocco finale con il portale di fine
        larghezza_blocco_finale = 200
        blocco_finale = Blocco(x_pos, self.ultima_altezza, larghezza_blocco_finale, 50, self.gioco.GROUND1)
        self.porzioni.append(blocco_finale)
        self.portale_fine = Portale(self.gioco, x_pos + larghezza_blocco_finale / 2, self.ultima_altezza - 55,
                                    self.colore_obbligatorio)
        # print(self.porzioni)

    def aggiorna(self):
        giocatore_x = self.gioco.giocatore.rect.x  # Ottieni la posizione x del giocatore
        self.porzione = None
        for porzione in self.porzioni:
            self.porzione = porzione
            porzione.rect.x += self.velocita
            # Check if the player has reached the block
            if giocatore_x > porzione.rect.x and not porzione.toccato:

                self.worm.emergi(porzione)  # Mark the block as touched

        for cristallo in self.cristalli:
            cristallo.rect.x += self.velocita

        for worm in self.worms:
            worm.rect.x += self.velocita
            #worm.emergi(self.porzione)

        if self.portale_inizio:
            self.portale_inizio.rect.x += self.velocita
        if self.portale_fine:
            self.portale_fine.rect.x += self.velocita

    def disegna(self, superficie):
        for worm in self.worms:
            worm.disegna(superficie)
        for porzione in self.porzioni:
            porzione.disegna(superficie)
        for cristallo in self.cristalli:
            cristallo.disegna(superficie)
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

    def genera_worm_per_porzione(self, porzione):
        if self.portale_fine and porzione == self.porzioni[-1]:
            # Non generare accelleratori su questa porzione se è destinata al portale di fine
            return
        if self.portale_inizio and porzione.rect.colliderect(self.portale_inizio.rect):
            return

        counter = random.randint(1, 2)
        if counter == 2:
            margine = 100  # Aumentato da 20 a 50 per tenere il buco nero lontano dai bordi
            x = random.randrange(porzione.left + margine, porzione.right - margine)
            y = porzione.top - self.worm.position  # Questo già posiziona l'Accelerator sopra la porzione

            # Assicurati che il costruttore di Accelerator accetti tutti i parametri necessari
            # Potrebbe essere necessario passare ulteriori parametri oltre a x e y, a seconda della tua implementazione
            self.worm = Worm(x, y)
            self.worms.add(self.worm)
        else:
            return
