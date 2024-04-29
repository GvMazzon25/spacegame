import sys
from Elements.Player import Giocatore, Giocatore2
from Elements.Coin import CoinManager
from Grounds.Ground import Terreno
from Grounds.Ground0 import Terreno0
from Grounds.Ground1 import Terreno1
from Grounds.Ground2 import Terreno2
from Grounds.Ground3 import Terreno3
from Grounds.Ground4 import Terreno4
import pygame
from Utility.configuration import Configurazione


class Level:
    def __init__(self, game_screen, configurazione, n, colore_iniziale=None):
        self.n_level = n
        self.config = Configurazione()
        self.game_screen = game_screen  # Aggiungi questo
        self.punteggio = 0
        self.schermo = game_screen.screen
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

        self.coin_manager = CoinManager(self, self.n_level)
        self.giocatore = Giocatore2(self, self) if self.n_level == 3 else Giocatore(self, self)
        self.ultimo_colore_cristallo = colore_iniziale  # Aggiungi questo

        self.terreno = self.scegli_terreno(n, colore_iniziale)
        self.livello_in_corso = True
        self.mode = configurazione['Rules']['MODE']
        self.image = configurazione['Image']
        sfondo_immagine = pygame.image.load(self.image).convert()  # Aggiorna con il percorso corretto dell'immagine
        self.SFONDO = pygame.transform.scale(sfondo_immagine, (self.LARGHEZZA, self.ALTEZZA))
        self.start_game_over_timer = None  # Nessun timer inizialmente

    def disegna_livello(self):
        """Ridisegna tutti gli elementi del livello sullo schermo."""
        self.schermo.blit(self.SFONDO, (0, 0))
        self.terreno.disegna(self.schermo)
        self.giocatore.disegna(self.schermo)
        self.coin_manager.disegna(self.schermo, self.n_level)
        if self.terreno.portale_fine:
            self.terreno.portale_fine.disegna(self.schermo)

        font = pygame.font.SysFont(None, 36)
        testo_punteggio = font.render(f"Punteggio: {self.punteggio}", True, (255, 255, 255))
        posizione_testo_punteggio_x = self.LARGHEZZA - testo_punteggio.get_width() - 10
        self.schermo.blit(testo_punteggio, (posizione_testo_punteggio_x, 10))

    def scegli_terreno(self, n, colore_iniziale):
        # Dizionario che mappa il numero del livello alla classe del terreno corrispondente
        mappa_terreni = {
            0: Terreno0,
            1: Terreno1,
            2: Terreno2,
            3: Terreno3,
            4: Terreno4
        }
        # Seleziona la classe del terreno basata sul numero del livello
        classe_terreno = mappa_terreni.get(n, Terreno)  # Fallback su Terreno se n non è nel dizionario
        # Istanzia e restituisce il terreno
        return classe_terreno(self, self.MAIN_COLOR, colore_iniziale=colore_iniziale)

    def esegui(self):
        while self.livello_in_corso and self.game_screen.gioco_in_corso:
            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif evento.type == pygame.KEYDOWN:
                    if evento.key == pygame.K_SPACE:
                        self.giocatore.salta()
                    # Da Cancellare ----------------------------------------
                    elif evento.key == pygame.K_RETURN:  # Se il tasto premuto è Invio
                        self.giocatore.cambia_colore(
                            self.MAIN_COLOR)  # Assicurati che questo metodo funzioni correttamente
                        self.terreno.portale_fine.cambia_colore(self.MAIN_COLOR)
                    # ------------------------------------------------------

            self.giocatore.aggiorna()
            self.terreno.aggiorna()
            self.coin_manager.aggiorna()
            self.coin_manager.gestisci_collisioni(self.giocatore)
            if self.n_level == 4:
                if self.terreno.plant is not None:
                    self.giocatore.verifica_collisione_con_plant()

            cristalli_toccati = pygame.sprite.spritecollide(self.giocatore, self.terreno.cristalli, True)
            for cristallo in cristalli_toccati:
                self.ultimo_colore_cristallo = cristallo.colore
                # Aggiorna anche il colore del giocatore se necessario
                self.giocatore.cambia_colore(cristallo.colore)
                # Aggiorna il colore del portale di fine, se esiste
                if self.terreno.portale_fine:
                    self.terreno.portale_fine.cambia_colore(cristallo.colore)

            if self.n_level == 0:
                black_hole_toccati = pygame.sprite.spritecollide(self.giocatore, self.terreno.buchi_neri, False)
                if black_hole_toccati and self.start_game_over_timer is None:
                    # Inizia il timer e avvia l'animazione dell'EventHorizon
                    self.start_game_over_timer = pygame.time.get_ticks()
                    for buco_nero in black_hole_toccati:
                        self.giocatore.nascondi()
                        buco_nero.inizia_animazione_event_horizon(self.game_screen.screen, self.clock,
                                                                  self.disegna_livello)
            if hasattr(self.terreno, 'funzione_verifica_accelerazione'):
                self.terreno.funzione_verifica_accelerazione()

            if self.n_level == 1:
                if not self.terreno.accellerator_on:
                    accellerators_toccati = pygame.sprite.spritecollide(self.giocatore, self.terreno.accellerators,
                                                                        False)
                    if accellerators_toccati:
                        for accelleratore in accellerators_toccati:
                            self.terreno.accelerazione()

            if self.n_level == 2:
                for worm in self.terreno.worms:
                    # Calculate the distance between the player and each worm
                    if abs(worm.rect.x - self.giocatore.rect.centerx) < 300:
                        worm.emergi(self.terreno.porzione)  # Call emergi if the distance is less than 300 px

                        # Check for collisions between the emerging worm and crystals
                        crystals_touched = pygame.sprite.spritecollide(worm, self.terreno.cristalli,
                                                                       True)  # True to kill the crystal
                        for crystal in crystals_touched:
                            crystal.kill()  # Remove the crystal if it is touched by the worm

                        # Check for collisions between the player and the worms
                        worm_toccati = pygame.sprite.spritecollide(self.giocatore, self.terreno.worms, False)
                        if worm_toccati:
                            for worm in worm_toccati:
                                self.game_over()

            if self.n_level == 3:
                gravity_toccati = pygame.sprite.spritecollide(self.giocatore, self.terreno.gravity_inverter_group,
                                                              False)
                if gravity_toccati:
                    for gravity in gravity_toccati:
                        self.giocatore.inverti_gravita()
                        self.giocatore.salta()

            # Controllo del timer per il game over
            if self.start_game_over_timer:
                time_passed = pygame.time.get_ticks() - self.start_game_over_timer
                if time_passed >= 1000:  # 1000 millisecondi = 1 secondo
                    self.game_over()
                    self.start_game_over_timer = None  # Reset del timer

            # Aggiorna le dimensioni dello schermo ogni volta che il ciclo viene eseguito
            self.LARGHEZZA, self.ALTEZZA = self.schermo.get_size()

            self.disegna_livello()

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
