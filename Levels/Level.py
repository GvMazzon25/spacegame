import pygame
import sys
from Utility.Exceptions import PerditaException
from Elements.Player import Giocatore
from Elements.Coin import CoinManager
from Elements.Ground import Terreno
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








# Classe Terreno
