import random
import pygame
from Elements.Portal import Portale
from Elements.Cristal import Cristallo


class Terreno:
    def __init__(self, gioco, colore_obbligatorio=None, colore_iniziale=None):
        self.gioco = gioco
        self.porzioni = []
        self.cristalli = pygame.sprite.Group()
        self.ultima_altezza = self.gioco.ALTEZZA - 50
        self.num_porzione_per_portale = random.randint(5, 20)
        # Usa il colore_iniziale per il portale di inizio, se specificato, altrimenti usa il colore predefinito del
        # gioco
        self.portale_inizio = Portale(self.gioco, 50, self.ultima_altezza - 75,
                                      colore_iniziale if colore_iniziale else self.gioco.AZZURRO)
        self.portale_fine = None  # Sarà impostato dopo la generazione delle porzioni
        self.colore_obbligatorio = colore_obbligatorio
        self.genera_terreno_iniziale()

    def genera_terreno_iniziale(self):
        larghezza_porz = random.randint(self.gioco.LARGHEZZA // 4, self.gioco.LARGHEZZA // 2)
        porzione_iniziale = pygame.Rect(0, self.ultima_altezza, larghezza_porz, 50)
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
        # Verifica se il portale di fine è già stato creato
        if self.portale_fine is not None:
            return  # Non generare nuovo terreno se il portale di fine esiste

        distanza_da_ultimo = random.randint(self.gioco.DISTANZA_ORIZZONTALE_MIN, self.gioco.DISTANZA_ORIZZONTALE_MAX)
        nuova_altezza = self.calcola_nuova_altezza()
        larghezza_nuova_porz = random.randint(self.gioco.LARGHEZZA // 4, self.gioco.LARGHEZZA // 2)
        ultima_porzione = self.porzioni[-1]
        nuova_porzione = pygame.Rect(ultima_porzione.right + distanza_da_ultimo, nuova_altezza, larghezza_nuova_porz,
                                     50)
        self.porzioni.append(nuova_porzione)

        # Genera ostacoli per ogni porzione (opzionale, a seconda della logica del tuo gioco)
        self.genera_cristallo_per_porzione(nuova_porzione, self.colore_obbligatorio)

        # Controlla se ci sono almeno due porzioni per generare i coin tra di loro
        if len(self.porzioni) > 1:
            porzione_prec = self.porzioni[-2]  # La penultima porzione
            porzione_succ = nuova_porzione  # L'ultima porzione appena aggiunta
            self.gioco.coin_manager.genera_coins_tra_terreni(porzione_prec, porzione_succ)

    def calcola_nuova_altezza(self):
        variazione_altezza = random.randint(-self.gioco.DIFFERENZA_ALTEZZA_MAX * 2,
                                            self.gioco.DIFFERENZA_ALTEZZA_MAX * 2)
        nuova_altezza = max(min(self.ultima_altezza + variazione_altezza, self.gioco.ALTEZZA - 100), 100)
        self.ultima_altezza = nuova_altezza
        return nuova_altezza

    def genera_cristallo_per_porzione(self, porzione, colore_obbligatorio=None):
        # Genera esattamente un cristallo per porzione.
        x = random.randrange(porzione.left + 20, porzione.right - 20)
        y = porzione.top - 60
        if self.colore_obbligatorio:
            cristallo = Cristallo(x, y, self.colore_obbligatorio)
        else:
            cristallo = Cristallo(x, y)
        self.cristalli.add(cristallo)

        # Dopo aver generato il primo cristallo con il colore obbligatorio,
        # puoi rimuovere il colore obbligatorio per le successive generazioni, se desideri
        self.colore_obbligatorio = None

    def aggiorna(self):
        # Muovi ogni porzione di terreno
        for porzione in self.porzioni:
            porzione.x += self.gioco.VELOCITA_TERRENO

        # Muovi ogni cristallo insieme al terreno
        for cristallo in self.cristalli:
            cristallo.rect.x += self.gioco.VELOCITA_TERRENO

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
            pygame.draw.rect(superficie, self.gioco.VERDE, porzione)
        for cristallo in self.cristalli:
            cristallo.disegna(superficie)
        self.portale_inizio.disegna(superficie)
        self.portale_fine.disegna(superficie)
