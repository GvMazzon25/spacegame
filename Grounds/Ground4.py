import random
import pygame
from Elements.Portal import Portale
from Elements.Cristal import Cristallo
from Elements.Blocco import Blocco
from SpecialElements.Plant import Plant


class Terreno4:
    def __init__(self, gioco, colore_obbligatorio, colore_iniziale=None, num_minimo_blocchi=10, num_massimo_blocchi=15):
        self.altezza_plant = 350
        self.plants = pygame.sprite.Group()
        self.plant = None
        self.altezza_fissa_count = 0
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
        self.plant_generato = False

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

        # Determina se questa porzione avrà altezza fissa o casuale
        usa_altezza_fissa = self.altezza_fissa_count > 0
        if usa_altezza_fissa:
            distanza_da_ultimo = random.randint(self.gioco.DISTANZA_ORIZZONTALE_MIN,
                                                self.gioco.DISTANZA_ORIZZONTALE_MAX)
            nuova_altezza = 300
            self.altezza_fissa_count -= 1  # Decrementa il contatore di altezze fisse
        else:
            # Decide casualmente se questa porzione sarà il punto di inizio per altezze fisse
            if random.randint(1, 2) == 1:
                distanza_da_ultimo = 0
                if random.randint(1, 2) == 1:
                    nuova_altezza = 300 + random.randint(5, 100)
                else:
                    nuova_altezza = 300 - random.randint(5, 100)
                self.altezza_fissa_count = 2  # Imposta un numero di porzioni consecutive ad altezza fissa
            else:
                nuova_altezza = self.calcola_nuova_altezza()
                distanza_da_ultimo = random.randint(self.gioco.DISTANZA_ORIZZONTALE_MIN,
                                                    self.gioco.DISTANZA_ORIZZONTALE_MAX)

        larghezza_nuova_porz = random.randint(self.gioco.LARGHEZZA // 4, self.gioco.LARGHEZZA // 2)
        ultima_porzione = self.porzioni[-1]

        nuova_porzione = Blocco(ultima_porzione.right + distanza_da_ultimo, nuova_altezza, larghezza_nuova_porz, 50,
                                self.gioco.GROUND1)

        self.altezza_plant = - (nuova_altezza - ultima_porzione.y - 90)
        if abs(- self.altezza_plant) > 250 and ultima_porzione.y > nuova_altezza:
            self.genera_plant_per_porzione(nuova_porzione, self.altezza_plant)
        self.porzioni.append(nuova_porzione)

        if len(self.porzioni) < self.num_porzione_per_portale:
            self.genera_cristallo_per_porzione(nuova_porzione)
        else:
            self.portale_fine = Portale(self.gioco, nuova_porzione.right + 50, nuova_porzione.top - 75,
                                        self.gioco.ultimo_colore_cristallo)

        # Genera i coin tra le porzioni solo se appropriato
        if len(self.porzioni) > 1 and abs(nuova_porzione.top - ultima_porzione.top) < 100:
            porzione_prec = self.porzioni[-2]
            porzione_succ = nuova_porzione
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

    def genera_plant_per_porzione(self, porzione, altezza_plant):
        x = porzione.left  # Usa il lato sinistro del blocco per il posizionamento
        y = porzione.top - Plant.position
        self.plant = Plant(x, y, altezza_plant)
        self.plants.add(self.plant)

    def aggiorna(self):
        # Muovi ogni porzione di terreno
        for porzione in self.porzioni:
            porzione.x += self.gioco.VELOCITA_TERRENO

        # Muovi ogni cristallo insieme al terreno
        for cristallo in self.cristalli:
            cristallo.rect.x += self.gioco.VELOCITA_TERRENO

        for plant in self.plants:
            plant.rect.x += self.gioco.VELOCITA_TERRENO

        # Muovi il portale di inizio insieme al terreno
        if self.portale_inizio:
            self.portale_inizio.rect.x += self.gioco.VELOCITA_TERRENO

        # Controlla se il portale di fine esiste e muovilo insieme al terreno
        if self.portale_fine:
            self.portale_fine.rect.x += self.gioco.VELOCITA_TERRENO

        # Rimuovi le porzioni che sono completamente fuori dallo schermo
        self.porzioni = [porzione for porzione in self.porzioni if porzione.right > 0]

        # Rimuovi i cristalli che sono completamente fuori dallo schermo
        for cristallo in self.cristalli:
            if cristallo.rect.right < 0:
                cristallo.kill()

        # Genera nuove porzioni e potenzialmente nuovi ostacoli se necessario
        if not self.porzioni or self.porzioni[-1].right < self.gioco.LARGHEZZA:
            self.aggiungi_porzione()

    def disegna(self, superficie):
        for porzione in self.porzioni:
            pygame.draw.rect(superficie, self.gioco.GROUND1, porzione)
        for cristallo in self.cristalli:
            cristallo.disegna(superficie)
        for plant in self.plants:
            plant.disegna(superficie)
        self.portale_inizio.disegna(superficie)
        self.portale_fine.disegna(superficie)
