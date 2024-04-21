import random
import pygame
from Elements.Portal import Portale
from Elements.Cristal import Cristallo
from Elements.Blocco import Blocco
from SpecialElements.BlackHole import BlackHole


class Terreno0:
    def __init__(self, gioco, colore_obbligatorio, colore_iniziale=None, num_minimo_blocchi=10, num_massimo_blocchi=15):
        self.buchi_neri = pygame.sprite.Group()
        self.buco_nero = BlackHole
        self.contatore_blackhole_generati = 0
        self.gioco = gioco
        self.porzioni = []
        self.cristalli = pygame.sprite.Group()
        self.ultima_altezza = self.gioco.ALTEZZA - 50
        self.num_minimo_blocchi = num_minimo_blocchi
        self.num_massimo_blocchi = num_massimo_blocchi
        self.num_porzione_per_portale = random.randint(self.num_minimo_blocchi, self.num_massimo_blocchi)
        self.portale_inizio = Portale(gioco, 50, self.ultima_altezza - 75,
                                      colore_iniziale if colore_iniziale else gioco.NEXT_COLOR)
        self.portale_fine = None  # Sarà impostato dopo la generazione delle porzioni
        self.colore_obbligatorio = colore_obbligatorio
        self.cristallo_colore_obbligatorio_generato = False  # Inizializza l'attributo qui
        self.contatore_cristalli_generati = 0
        # Decidi in modo casuale in quale chiamata generare il cristallo obbligatorio
        self.chiamata_per_cristallo_obbligatorio = random.randint(1, 5)
        self.rainbow_locale = list(Cristallo.RAINBOW)  # Crea una copia locale della lista dei colori arcobaleno
        self.porzioni = []

        if colore_obbligatorio in self.rainbow_locale:
            self.rainbow_locale.remove(colore_obbligatorio)
        self.genera_terreno_iniziale()

    def genera_terreno_iniziale(self):
        x_pos = 0
        larghezza_porz = random.randint(self.gioco.LARGHEZZA // 4, self.gioco.LARGHEZZA // 2)
        porzione_iniziale = Blocco(x_pos, self.ultima_altezza - 75, larghezza_porz, 50, self.gioco.GROUND1)
        self.porzioni.append(porzione_iniziale)

        # Assumi di voler generare il numero di porzioni specificato da num_porzione_per_portale
        # meno la porzione iniziale già aggiunta
        for _ in range(1, self.num_porzione_per_portale):
            self.aggiungi_porzione()

        # Ora che tutte le porzioni sono state generate, posiziona il portale di fine
        ultima_porzione = self.porzioni[-1]
        self.portale_fine = Portale(self.gioco, ultima_porzione.right + 50, ultima_porzione.top - 75,
                                    self.gioco.ultimo_colore_cristallo)

    def aggiungi_porzione(self):
        if self.portale_fine is not None:
            # Non generare nuovo terreno se il portale di fine esiste già
            return

        distanza_da_ultimo = random.randint(self.gioco.DISTANZA_ORIZZONTALE_MIN, self.gioco.DISTANZA_ORIZZONTALE_MAX)
        nuova_altezza = self.calcola_nuova_altezza()
        larghezza_nuova_porz = random.randint(self.gioco.LARGHEZZA // 4, self.gioco.LARGHEZZA // 2)
        ultima_porzione = self.porzioni[-1]
        nuova_porzione = Blocco(ultima_porzione.right + distanza_da_ultimo, nuova_altezza, larghezza_nuova_porz,
                                50, self.gioco.GROUND1)
        self.porzioni.append(nuova_porzione)
        # print(nuova_porzione)
        # Se questa è l'ultima porzione prima del portale di fine, non generare cristalli
        if len(self.porzioni) < self.num_porzione_per_portale:
            self.genera_cristallo_per_porzione(nuova_porzione)
            self.genera_blackhole_per_porzione(nuova_porzione)
        else:
            # Qui potresti voler generare il portale di fine invece di un cristallo
            self.portale_fine = Portale(self.gioco, nuova_porzione.right + 50, nuova_porzione.top - 75,
                                        self.gioco.ultimo_colore_cristallo)

        # Genera i coin tra le porzioni, se applicabile
        if len(self.porzioni) > 1:
            porzione_prec = self.porzioni[-2]  # La penultima porzione
            porzione_succ = nuova_porzione  # L'ultima porzione appena aggiunta
            self.gioco.coin_manager.genera_coins_tra_terreni(porzione_prec, porzione_succ, False)

    def calcola_nuova_altezza(self):
        variazione_altezza = random.randint(-self.gioco.DIFFERENZA_ALTEZZA_MAX * 2,
                                            self.gioco.DIFFERENZA_ALTEZZA_MAX * 2)
        nuova_altezza = max(min(self.ultima_altezza + variazione_altezza, self.gioco.ALTEZZA - 100), 100)
        self.ultima_altezza = nuova_altezza
        return nuova_altezza

    def genera_cristallo_per_porzione(self, porzione):
        if self.portale_fine and porzione == self.porzioni[-1]:
            # Non generare cristalli su questa porzione se è destinata al portale di fine
            return

        self.contatore_cristalli_generati += 1
        x = random.randrange(porzione.left + 20, porzione.right - 20)
        y = porzione.top - 60

        if not self.cristallo_colore_obbligatorio_generato and self.contatore_cristalli_generati == self.chiamata_per_cristallo_obbligatorio:
            cristallo = Cristallo(x, y, self.colore_obbligatorio)
            self.cristallo_colore_obbligatorio_generato = True
        else:
            colore_random = random.choice(self.rainbow_locale)  # Usa la copia locale per scegliere un colore casuale
            cristallo = Cristallo(x, y, colore_random)

        self.cristalli.add(cristallo)

    def genera_blackhole_per_porzione(self, porzione):
        if self.portale_fine and porzione == self.porzioni[-1]:
            # Non generare cristalli su questa porzione se è destinata al portale di fine
            return

        counter = random.randint(1, 2)
        if counter == 2:
            self.contatore_blackhole_generati += 1
            margine = 100  # Aumentato da 20 a 50 per tenere il buco nero lontano dai bordi
            x = random.randrange(porzione.left + margine, porzione.right - margine)
            y = porzione.top - 60
            self.buco_nero = BlackHole(x, y)

            self.buchi_neri.add(self.buco_nero)
        else:
            return

    def aggiorna(self):
        # Muovi ogni porzione di terreno
        velocita_terreno = self.gioco.VELOCITA_TERRENO
        for porzione in self.porzioni:
            porzione.x += velocita_terreno

        # Muovi ogni cristallo insieme al terreno
        for cristallo in self.cristalli:
            cristallo.rect.x += velocita_terreno

        for buco_nero in self.buchi_neri:
            buco_nero.update_position(velocita_terreno)

        # Muovi il portale di inizio insieme al terreno
        if self.portale_inizio:
            self.portale_inizio.rect.x += velocita_terreno

        # Controlla se il portale di fine esiste e muovilo insieme al terreno
        if self.portale_fine:
            self.portale_fine.rect.x += velocita_terreno

        # Rimuovi le porzioni che sono completamente fuori dallo schermo
        self.porzioni = [porzione for porzione in self.porzioni if porzione.right > 0]

        # Rimuovi i cristalli che sono completamente fuori dallo schermo
        for cristallo in self.cristalli:
            if cristallo.rect.right < 0:
                cristallo.kill()

        for cristallo in self.cristalli:
            hole_touched = pygame.sprite.spritecollide(cristallo, self.buchi_neri, False)
            if hole_touched:
                cristallo.kill()
                if cristallo.color() == self.gioco.NEXT_COLOR:
                    self.rainbow_locale.append(self.colore_obbligatorio)
                    self.cristallo_colore_obbligatorio_generato = False

        for buco_nero in self.buchi_neri:
            if buco_nero.rect.right < 0:
                buco_nero.kill()

        # Genera nuove porzioni e potenzialmente nuovi ostacoli se necessario
        if not self.porzioni or self.porzioni[-1].right < self.gioco.LARGHEZZA:
            self.aggiungi_porzione()

    def disegna(self, superficie):
        for porzione in self.porzioni:
            pygame.draw.rect(superficie, self.gioco.GROUND1, porzione)
        for cristallo in self.cristalli:
            cristallo.disegna(superficie)
        for buco_nero in self.buchi_neri:
            buco_nero.disegna(superficie)
        self.portale_inizio.disegna(superficie)
        self.portale_fine.disegna(superficie)
