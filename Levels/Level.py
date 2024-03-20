import pygame
import sys
import random
from Utility.Exceptions import PerditaException


class Livello:
    def __init__(self, schermo, configurazione, colore_iniziale=None):
        pygame.init()
        self.punteggio = 0

        self.schermo = schermo
        self.LARGHEZZA, self.ALTEZZA = self.schermo.get_size()
        self.clock = pygame.time.Clock()

        self.NERO = configurazione['SFONDO']
        self.BLU = configurazione['SKIN']
        self.VERDE = configurazione['TERRENO']
        self.ROSSO = configurazione['ROSSO']
        self.AZZURRO = configurazione['AZZURRO']

        self.VELOCITA_TERRENO = configurazione['VELOCITA_TERRENO']
        self.DISTANZA_ORIZZONTALE_MIN = configurazione['DISTANZA_ORIZZONTALE_MIN']
        self.DISTANZA_ORIZZONTALE_MAX = configurazione['DISTANZA_ORIZZONTALE_MAX']
        self.DIFFERENZA_ALTEZZA_MAX = configurazione['DIFFERENZA_ALTEZZA_MAX']
        self.SALTO_MAX = configurazione['SALTO_MAX']
        self.MAIN_COLOR = configurazione.get("MAIN_COLOR")

        self.coin_manager = CoinManager(self)
        self.giocatore = Giocatore(self,self)
        self.ultimo_colore_cristallo = colore_iniziale  # Aggiungi questo

        self.terreno = Terreno(self, colore_obbligatorio=configurazione.get("MAIN_COLOR"),
                               colore_iniziale=colore_iniziale)

    def esegui(self):
        completato = False
        while not completato:
            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif evento.type == pygame.KEYDOWN:
                    if evento.key == pygame.K_SPACE:
                        self.giocatore.salta()

            self.giocatore.aggiorna()
            self.terreno.aggiorna()
            self.coin_manager.aggiorna()
            self.coin_manager.gestisci_collisioni(self.giocatore)

            cristalli_toccati = pygame.sprite.spritecollide(self.giocatore, self.terreno.cristalli, True)
            for cristallo in cristalli_toccati:
                self.ultimo_colore_cristallo = cristallo.color
                # Aggiorna anche il colore del giocatore se necessario
                self.giocatore.cambia_colore(cristallo.color)
                # Aggiorna il colore del portale di fine, se esiste
                if self.terreno.portale_fine:
                    self.terreno.portale_fine.cambia_colore(cristallo.color)

            self.schermo.fill(self.NERO)
            self.terreno.disegna(self.schermo)
            self.giocatore.disegna(self.schermo)
            self.coin_manager.disegna(self.schermo)
            if self.terreno.portale_fine:
                self.terreno.portale_fine.disegna(self.schermo)

            font = pygame.font.SysFont(None, 36)
            testo_punteggio = font.render(f"Punteggio: {self.punteggio}", True, (255, 255, 255))
            self.schermo.blit(testo_punteggio, (self.LARGHEZZA - testo_punteggio.get_width() - 10, 10))

            pygame.display.flip()
            self.clock.tick(30)

            if self.terreno.portale_fine and self.giocatore.rect.colliderect(self.terreno.portale_fine.rect):
                if self.terreno.portale_fine.colore == self.MAIN_COLOR:  # Verifica il colore del portale
                    completato = self.livello_superato()
                else:
                    print("Hai perso! Il colore del portale non corrisponde al colore richiesto.")
                    # Al posto di chiudere il gioco, solleva un'eccezione
                    raise PerditaException(self.punteggio)

        return completato

    def obtain_score(self):
        return self.punteggio

    def livello_superato(self):
        # Mostra un messaggio o esegui un'animazione qui
        # Non chiamare più pygame.quit() o sys.exit() qui
        # Al termine, restituisci True per segnalare che il livello è stato superato
        font = pygame.font.Font(None, 74)
        testo = font.render("Livello superato!", 1, (255, 255, 255))
        testo_pos = testo.get_rect(centerx=self.schermo.get_width() / 2, centery=self.schermo.get_height() / 2)
        self.schermo.blit(testo, testo_pos)
        pygame.display.flip()
        pygame.time.wait(2000)  # Attendi un po' prima di passare al livello successivo

        return True


# Classe Giocatore


def game_over(livello):
    print("Hai perso!")
    score = livello.obtain_score()
    print(score)
    raise PerditaException(score)


class Giocatore(pygame.sprite.Sprite):
    def __init__(self, gioco,livello):
        super().__init__()
        self.gioco = gioco
        self.surf = pygame.Surface((50, 50))
        self.colore_corrente = self.surf.fill(self.gioco.BLU)
        self.rect = self.surf.get_rect(center=(self.gioco.LARGHEZZA // 8, self.gioco.ALTEZZA - 150))
        self.livello = livello
        self.velocita_y = 1
        self.salti_rimanenti = 2

    def cambia_colore(self, nuovo_colore):
        self.colore_corrente = self.surf.fill(nuovo_colore)
        self.surf.fill(nuovo_colore)

    def aggiorna(self):
        self.velocita_y += 1  # Simula la gravità
        self.rect.y += self.velocita_y  # Aggiorna la posizione verticale

        # Verifica collisione con il terreno e aggiorna di conseguenza
        self.verifica_collisione_con_terreno()

    def verifica_collisione_con_terreno(self):
        self.rect.y += 1  # Piccolo spostamento verso il basso per facilitare la verifica delle collisioni
        collisioni = [porzione for porzione in self.gioco.terreno.porzioni if self.rect.colliderect(porzione)]

        if collisioni:
            self.rect.bottom = collisioni[0].top
            self.velocita_y = 0
            self.salti_rimanenti = 2
        else:
            # Se non ci sono collisioni e il giocatore è sotto un certo limite, ha perso
            if self.rect.top > self.gioco.ALTEZZA:
                game_over(self.livello)

        self.rect.y -= 1  # Ripristina la posizione originale se non c'è stata collisione

    def salta(self):
        if self.salti_rimanenti > 0:
            self.velocita_y = -20
            self.salti_rimanenti -= 1

    def disegna(self, superficie):
        superficie.blit(self.surf, self.rect)

    def vittoria(self):
        print("Hai vinto!")
        pygame.quit()
        sys.exit()


# Classe Ostacolo
class Cristallo(pygame.sprite.Sprite):
    COLORI = [
        (255, 0, 0),  # Rosso
        (255, 165, 0),  # Arancione
        (255, 255, 0),  # Giallo
        (0, 128, 0),  # Verde
        (0, 0, 255),  # Blu
        (128, 0, 128),  # Viola
        (75, 0, 130)  # Indaco
    ]

    def __init__(self, x, y, color=None):
        super().__init__()
        # Se non viene specificato un colore, ne sceglie uno casualmente dalla lista COLORI
        self.color = color if color is not None else random.choice(Cristallo.COLORI)
        self.surf = pygame.Surface((20, 40), pygame.SRCALPHA)  # Dimensioni del rombo
        pygame.draw.polygon(self.surf, self.color, [(10, 0), (20, 20), (10, 40), (0, 20)])  # Disegna un rombo
        self.rect = self.surf.get_rect(center=(x, y))

    def disegna(self, superficie):
        superficie.blit(self.surf, self.rect)


class Portale(pygame.sprite.Sprite):
    def __init__(self, gioco, x, y, colore_iniziale):
        super().__init__()
        self.gioco = gioco
        self.surf = pygame.Surface((20, 100))
        self.colore = colore_iniziale if colore_iniziale is not None else (0, 255, 255)  # Esempio di colore di default
        self.surf.fill(self.colore)
        self.rect = self.surf.get_rect(center=(x, y))

    def disegna(self, superficie):
        superficie.blit(self.surf, self.rect)

    def cambia_colore(self, nuovo_colore):
        self.colore = nuovo_colore  # Aggiorna il colore memorizzato
        self.surf.fill(self.colore)


class Coin(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.surf = pygame.Surface((10, 10))  # Dimensioni del coin
        self.surf.fill((255, 255, 0))  # Colore giallo per il coin
        self.rect = self.surf.get_rect(center=(x, y))

    def disegna(self, superficie):
        superficie.blit(self.surf, self.rect)


class CoinManager:
    def __init__(self, gioco):
        self.gioco = gioco
        self.coins = pygame.sprite.Group()

    def genera_coins_tra_terreni(self, porzione_prec, porzione_succ):
        start_x = porzione_prec.right
        end_x = porzione_succ.left
        ground_y = max(porzione_prec.bottom, porzione_succ.bottom)
        peak_y = min(porzione_prec.top, porzione_succ.top) - 150  # Altezza del vertice della parabola
        num_coins = 15  # Numero di coin

        # Definiamo un offset per sollevare i punti di inizio e fine della parabola
        start_end_offset = 30  # Solleva di 20 pixel sopra la linea del terreno

        # Calcolo della larghezza della traiettoria parabolica e dell'altezza
        width = end_x - start_x
        height = peak_y - ground_y + start_end_offset

        for i in range(num_coins):
            # Normalizza la posizione dei coin lungo l'asse x
            normalized_x = (i / (num_coins - 1)) - 0.5  # -0.5 a 0.5
            # Calcola la posizione x del coin
            x = start_x + (i / (num_coins - 1)) * width
            # Calcola la posizione y del coin usando una formula parabolica semplice
            y = peak_y - 4 * height * (normalized_x ** 2) - start_end_offset

            self.coins.add(Coin(x, y))

    def aggiorna(self):
        # Muovi i coin insieme al terreno
        for coin in self.coins:
            coin.rect.x += self.gioco.VELOCITA_TERRENO
            # Se un coin esce dallo schermo, viene eliminato
            if coin.rect.right < 0:
                coin.kill()

    def gestisci_collisioni(self, giocatore):
        coins_colpiti = pygame.sprite.spritecollide(giocatore, self.coins, True)
        if coins_colpiti:
            self.gioco.punteggio += len(coins_colpiti)

    def disegna(self, superficie):
        for coin in self.coins:
            coin.disegna(superficie)


# Classe Terreno
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
