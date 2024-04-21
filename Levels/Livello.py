import sys
from Elements.Player import Giocatore
from Elements.Coin import CoinManager
from Grounds.Ground import Terreno
import pygame
from Utility.configuration import Configurazione


class Livello:
    def __init__(self, game_screen, configurazione, n, colore_iniziale=None):
        self.n_level = n
        self.config = Configurazione()
        self.game_screen = game_screen  # Aggiungi questo
        self.punteggio = 0
        self.schermo = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        self.LARGHEZZA, self.ALTEZZA = self.schermo.get_size()
        self.clock = pygame.time.Clock()

        self.SFONDO = configurazione['Palette']['SFONDO']
        self.SKIN = configurazione['Palette']['SKIN']
        self.GROUND1 = configurazione['Palette']['TERRENO']
        self.ROSSO = configurazione['Palette']['ROSSO']
        self.NEXT_COLOR = configurazione['Palette']['NEXT_COLOR']

        self.VELOCITA_TERRENO = configurazione['Rules']['VELOCITA_TERRENO']
        self.DISTANZA_ORIZZONTALE_MIN = configurazione['Rules']['DISTANZA_ORIZZONTALE_MIN']
        self.DISTANZA_ORIZZONTALE_MAX = configurazione['Rules']['DISTANZA_ORIZZONTALE_MAX']
        self.DIFFERENZA_ALTEZZA_MAX = configurazione['Rules']['DIFFERENZA_ALTEZZA_MAX']
        self.SALTO_MAX = configurazione['Rules']['SALTO_MAX']
        self.MAIN_COLOR = configurazione['Palette']['MAIN_COLOR']

        self.coin_manager = CoinManager(self)
        self.giocatore = Giocatore(self, self)
        self.ultimo_colore_cristallo = colore_iniziale  # Aggiungi questo

        self.terreno = Terreno(self, self.MAIN_COLOR,
                               colore_iniziale=colore_iniziale)
        self.livello_in_corso = True
        self.mode = configurazione['Rules']['MODE']
        self.image = configurazione['Image']
        sfondo_immagine = pygame.image.load(self.image).convert()  # Aggiorna con il percorso corretto dell'immagine
        self.SFONDO = pygame.transform.scale(sfondo_immagine, (self.LARGHEZZA, self.ALTEZZA))

    def esegui(self):
        while self.livello_in_corso and self.game_screen.gioco_in_corso:
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
                self.ultimo_colore_cristallo = cristallo.colore
                # Aggiorna anche il colore del giocatore se necessario
                self.giocatore.cambia_colore(cristallo.colore)
                # Aggiorna il colore del portale di fine, se esiste
                if self.terreno.portale_fine:
                    self.terreno.portale_fine.cambia_colore(cristallo.colore)

            # Aggiorna le dimensioni dello schermo ogni volta che il ciclo viene eseguito
            self.LARGHEZZA, self.ALTEZZA = self.schermo.get_size()

            self.schermo.blit(self.SFONDO, (0, 0))
            self.terreno.disegna(self.schermo)
            self.giocatore.disegna(self.schermo)
            self.coin_manager.disegna(self.schermo)
            if self.terreno.portale_fine:
                self.terreno.portale_fine.disegna(self.schermo)

            font = pygame.font.SysFont(None, 36)
            testo_punteggio = font.render(f"Punteggio: {self.punteggio}", True, (255, 255, 255))
            self.schermo.blit(testo_punteggio, (self.LARGHEZZA - testo_punteggio.get_width() - 10, 10))
            # Calcola la posizione del testo in base alla larghezza attuale della finestra
            posizione_testo_punteggio_x = self.LARGHEZZA - testo_punteggio.get_width() - 10
            self.schermo.blit(testo_punteggio, (posizione_testo_punteggio_x, 10))

            pygame.display.flip()
            self.clock.tick(30)

            if self.terreno.portale_fine and self.giocatore.rect.colliderect(self.terreno.portale_fine.rect):
                if self.terreno.portale_fine.colore == self.MAIN_COLOR:
                    return self.vittoria()
                else:
                    self.config.replace_score(self.punteggio)
                    return self.game_over()

    def game_over(self):
        """Gestisce la logica di game over per il livello."""
        print("Game Over")
        self.game_screen.gioco_in_corso = False  # Aggiorna lo stato del gioco
        self.livello_in_corso = False
        return "sconfitta"  # Aggiungi il ritorno di "sconfitta"

    def vittoria(self):
        """Gestisce la logica di vittoria per il livello."""
        print("Vittoria!")
        self.config.replace_score(self.punteggio)
        self.config.replace_level_passed(self.n_level + 1)
        self.game_screen.gioco_in_corso = True
        return "vittoria"

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
