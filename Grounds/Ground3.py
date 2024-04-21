import random
import pygame
from Elements.Portal import Portale
from Elements.Cristal import Cristallo
from Elements.Blocco import Blocco
from SpecialElements.gravity_inverter import GravityInverter


class Terreno3:
    def __init__(self, gioco, colore_obbligatorio, colore_iniziale=None, num_minimo_blocchi=10, num_massimo_blocchi=15):
        self.gravity_inverter_group = pygame.sprite.Group()
        self.gravity_inverter = GravityInverter
        self.contatore_gravity_generati = 0
        self.gioco = gioco
        self.porzioni = []
        self.porzioni_inferiori = []  # Terreno inferiore
        self.cristalli = pygame.sprite.Group()
        self.ultima_altezza = 50
        self.num_minimo_blocchi = num_minimo_blocchi
        self.num_massimo_blocchi = num_massimo_blocchi
        self.num_porzione_per_portale = random.randint(self.num_minimo_blocchi, self.num_massimo_blocchi)
        self.portale_inizio = Portale(gioco, 90, 170, colore_iniziale if colore_iniziale else gioco.NEXT_COLOR)
        self.portale_fine = None  # Sarà impostato dopo la generazione delle porzioni
        self.colore_obbligatorio = colore_obbligatorio
        self.colore_iniziale = colore_iniziale
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
        larghezza_porz = random.randint(self.gioco.LARGHEZZA // 4, self.gioco.LARGHEZZA // 2)
        # Terreno superiore
        porzione_superiore = Blocco(0, self.ultima_altezza, larghezza_porz, 50, self.gioco.GROUND1)
        self.porzioni.append(porzione_superiore)
        # Terreno inferiore
        porzione_inferiore = Blocco(0, self.gioco.ALTEZZA - self.ultima_altezza - 50, larghezza_porz, 50,
                                    self.gioco.GROUND1)
        self.porzioni_inferiori.append(porzione_inferiore)

        for _ in range(1, self.num_porzione_per_portale):
            self.aggiungi_porzione()
            self.aggiungi_porzione_inferiore()

        if random.choice([True, False]):
            # Posiziona il portale di fine nel terreno superiore
            ultima_superiore = self.porzioni[-1]
            self.portale_fine = Portale(self.gioco, ultima_superiore.right + 50, ultima_superiore.bottom + 75,
                                        self.gioco.ultimo_colore_cristallo)
        else:
            # Posiziona il portale di fine nel terreno inferiore, sopra il bordo superiore di esso
            ultima_inferiore = self.porzioni_inferiori[-1]
            self.portale_fine = Portale(self.gioco, ultima_inferiore.right + 50, ultima_inferiore.top - 75,
                                        self.gioco.ultimo_colore_cristallo)

    def aggiungi_porzione(self):
        if self.portale_fine:
            return

        nuova_altezza = self.calcola_nuova_altezza()
        larghezza_nuova_porz = random.randint(self.gioco.LARGHEZZA // 4, self.gioco.LARGHEZZA // 2)
        ultima_porzione = self.porzioni[-1]
        nuova_porzione = Blocco(ultima_porzione.right + random.randint(self.gioco.DISTANZA_ORIZZONTALE_MIN,
                                                                       self.gioco.DISTANZA_ORIZZONTALE_MAX),
                                nuova_altezza, larghezza_nuova_porz, 50, self.gioco.GROUND1)
        self.porzioni.append(nuova_porzione)
        if len(self.porzioni) < self.num_porzione_per_portale:
            self.genera_elementi(nuova_porzione, self.porzioni[-2], self.porzioni, True)

    def aggiungi_porzione_inferiore(self):
        nuova_altezza = self.gioco.ALTEZZA - self.ultima_altezza - 50
        larghezza_nuova_porz = random.randint(self.gioco.LARGHEZZA // 4, self.gioco.LARGHEZZA // 2)
        ultima_porzione = self.porzioni_inferiori[-1]
        nuova_porzione = Blocco(ultima_porzione.right + random.randint(self.gioco.DISTANZA_ORIZZONTALE_MIN,
                                                                       self.gioco.DISTANZA_ORIZZONTALE_MAX),
                                nuova_altezza, larghezza_nuova_porz, 50, self.gioco.GROUND1)
        self.porzioni_inferiori.append(nuova_porzione)
        if len(self.porzioni_inferiori) < self.num_porzione_per_portale:
            self.genera_elementi(nuova_porzione, self.porzioni_inferiori[-2], self.porzioni_inferiori, False)

    def genera_elementi(self, nuova_porzione, porzione_prec, porzioni_list, up_down):
        # Genera cristalli, buchi neri e monete
        if up_down:
            self.genera_cristallo_per_porzione(nuova_porzione, True)
            self.genera_gravity_per_porzione(nuova_porzione, True)
            self.gioco.coin_manager.genera_coins_tra_terreni(porzione_prec, nuova_porzione, True)
        else:
            self.genera_cristallo_per_porzione(nuova_porzione, False)
            self.genera_gravity_per_porzione(nuova_porzione, False)
            self.gioco.coin_manager.genera_coins_tra_terreni(porzione_prec, nuova_porzione, False)

    def calcola_nuova_altezza(self):
        variazione_altezza = random.randint(-self.gioco.DIFFERENZA_ALTEZZA_MAX, self.gioco.DIFFERENZA_ALTEZZA_MAX)
        nuova_altezza = max(min(self.ultima_altezza + variazione_altezza, self.gioco.ALTEZZA - 100), 50)
        self.ultima_altezza = nuova_altezza
        return nuova_altezza

    def genera_cristallo_per_porzione(self, porzione, up_down):
        if self.portale_fine and porzione == self.porzioni[-1]:
            # Non generare cristalli su questa porzione se è destinata al portale di fine
            return

        self.contatore_cristalli_generati += 1
        x = random.randrange(porzione.left + 20, porzione.right - 20)
        if up_down:
            y = porzione.bottom + 50
        else:
            y = porzione.top - 60

        if not self.cristallo_colore_obbligatorio_generato and self.contatore_cristalli_generati == self.chiamata_per_cristallo_obbligatorio:
            cristallo = Cristallo(x, y, self.colore_obbligatorio)
            self.cristallo_colore_obbligatorio_generato = True
        else:
            colore_random = random.choice(self.rainbow_locale)
            cristallo = Cristallo(x, y, colore_random)

        self.cristalli.add(cristallo)

    def genera_gravity_per_porzione(self, porzione, up_down):
        if self.portale_fine and porzione == self.porzioni[-1]:
            # Non generare cristalli su questa porzione se è destinata al portale di fine
            return

        counter = random.randint(1, 2)
        if counter == 2:
            self.contatore_gravity_generati += 1
            margine = 100
            x = random.randrange(porzione.left + margine, porzione.right - margine)
            if up_down:
                y = porzione.bottom + 50
            else:
                y = porzione.top - 60
            self.gravity_inverter = GravityInverter(x, y)

            self.gravity_inverter_group.add(self.gravity_inverter)
        else:
            return

    def aggiorna(self):
        # Muovi ogni porzione di terreno
        velocita_terreno = self.gioco.VELOCITA_TERRENO
        for porzione in self.porzioni:
            porzione.x += velocita_terreno

        for porzione in self.porzioni_inferiori:
            porzione.x += velocita_terreno

        # Muovi ogni cristallo insieme al terreno
        for cristallo in self.cristalli:
            cristallo.rect.x += velocita_terreno

        for gravity in self.gravity_inverter_group:
            gravity.rect.x += velocita_terreno

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
            gravity_touched = pygame.sprite.spritecollide(cristallo, self.gravity_inverter_group, False)
            if gravity_touched:
                cristallo.kill()
                if cristallo.color() == self.gioco.NEXT_COLOR:
                    self.rainbow_locale.append(self.colore_obbligatorio)
                    self.cristallo_colore_obbligatorio_generato = False

        for gravity in self.gravity_inverter_group:
            if gravity.rect.right < 0:
                gravity.kill()

        # Genera nuove porzioni e potenzialmente nuovi ostacoli se necessario
        if not self.porzioni or self.porzioni[-1].right < self.gioco.LARGHEZZA:
            self.aggiungi_porzione()

    def disegna(self, superficie):
        # Disegna entrambi i terreni

        for porzione in self.porzioni:
            pygame.draw.rect(superficie, self.gioco.GROUND1, porzione)
        for porzione in self.porzioni_inferiori:
            pygame.draw.rect(superficie, self.gioco.GROUND1, porzione)
        for cristallo in self.cristalli:
            cristallo.disegna(superficie)
        for gravity in self.gravity_inverter_group:
            gravity.disegna(superficie)
        self.portale_inizio.disegna(superficie)
        if self.portale_fine:
            self.portale_fine.disegna(superficie)


