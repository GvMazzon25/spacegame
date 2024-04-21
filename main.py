import pygame
import sys
from Screen.first_screen import FirstScreen
from Screen.Menu import MainMenu
from Utility.configuration import Configurazione
from Levels.Livello import Livello
from Screen.load_screen import LoadingScreen
from Screen.schermata_sconfitta import SchermataSconfitta
from Screen.schermata_vittoria import SchermataVittoria
from Screen.schermata_scelta import FinestraScelta
from Levels.Level import Level


class GameScreen:
    def __init__(self, width=800, height=600):
        self.loading_start_time = None
        self.screen_switch_time = pygame.time.get_ticks() + 3000
        self.livelli = []
        self.ultimo_livello_raggiunto = 0
        self.livello_attuale = 0
        self.configurazione = Configurazione()
        pygame.init()
        self.info = pygame.display.Info()
        # Altezza del display
        self.altezza_display = self.info.current_h
        # Larghezza del display
        self.larghezza_display = self.info.current_w
        self.LARGHEZZA, self.ALTEZZA = width, height
        self.display_info = pygame.display.Info()  # Ottiene le informazioni dello schermo
        self.fullscreen_size = (
            self.display_info.current_w, self.display_info.current_h)  # Dimensioni per fullscreen "finto"
        self.screen = pygame.display.set_mode(self.fullscreen_size, pygame.RESIZABLE)
        self.clock = pygame.time.Clock()
        pygame.display.set_caption("Infinity: The Impossible Game")
        self.fullscreen = True  # Si inizia direttamente in modalità full screen "finto"
        self.first_screen = FirstScreen(self.screen)
        self.main_menu = MainMenu(self.screen)
        self.loading_screen = LoadingScreen(self.screen)
        self.schermata_sconfitta = SchermataSconfitta(self.screen)
        self.schermata_vittoria = SchermataVittoria(self.screen)
        self.schermata_scelta = FinestraScelta(self.screen)
        self.current_screen = self.first_screen
        self.show_loading = False
        self.menu_selection = 0  # Variabile per tenere traccia della selezione nel menu
        self.gioco_in_corso = True

        # TEST
        self.livelli_prova = []

    def mostra_menu_principale(self):
        """Mostra il menu principale e ritorna la modalità selezionata."""
        running = True
        modalita_selezionata = 0  # Valore di default se nessuna selezione è fatta

        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    # Ottiene la posizione del click e chiama handle_click
                    modalita_selezionata = self.main_menu.handle_click(event.pos)
                    if modalita_selezionata:
                        running = False  # Esce dal ciclo se una modalità è stata selezionata

            self.main_menu.draw()  # Continua a disegnare il menu principale
            pygame.display.flip()
            self.clock.tick(60)

        # Mappa il valore numerico restituito al nome della modalità
        if modalita_selezionata == 1:  # DIFFICILE
            self.inizializza_gioco_facile()
            return "DIFFICILE"
        elif modalita_selezionata in [2, 3]:  # MEDIO o FACILE
            self.inizializza_gioco_standard()
            return "MEDIO" if modalita_selezionata == 2 else "FACILE"
        else:
            return None

    def toggle_fullscreen(self):
        # Questa funzione ora imposta la modalità full screen "finto" all'avvio del gioco
        if not self.fullscreen:
            self.screen = pygame.display.set_mode(self.fullscreen_size, pygame.RESIZABLE)
            self.fullscreen = True
        # Non è necessario gestire il passaggio a modalità finestra perché il gioco rimane in full screen "finto"

    def reset_gioco(self):
        print('ciao')
        """Resetta lo stato del gioco mantenendo la modalità full screen "finto"."""
        self.configurazione.reset_modality()
        self.inizializza_gioco_standard()
        self.gioco_in_corso = True
        self.livello_attuale = 0
        self.ultimo_livello_raggiunto = 0
        self.show_loading = False
        self.toggle_fullscreen()

    def inizializza_gioco_standard(self):
        configurazioni = self.configurazione.genera_lista_strutture()
        self.livelli = [Level(self, config, indice) for indice, config in enumerate(configurazioni)]

    def inizializza_gioco_facile(self):
        configurazioni = self.configurazione.genera_lista_strutture()
        self.livelli = [Livello(self, config, indice) for indice, config in enumerate(configurazioni)]

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN and self.current_screen == self.main_menu:
                if event.button == 1:  # Click sinistro
                    # Gestione del click nei pulsanti del menu principale
                    self.menu_selection = self.main_menu.handle_click(event.pos)

    def update(self):
        current_ticks = pygame.time.get_ticks()
        if self.show_loading and current_ticks - self.loading_start_time > 3000:  # Mostra la schermata di caricamento per 3 secondi
            self.show_loading = False
            # Qui puoi aggiungere la logica per cambiare alla schermata del gioco effettivo in base alla selezione
        elif current_ticks >= self.screen_switch_time and self.current_screen == self.first_screen:
            self.current_screen = self.main_menu  # Passa al MainMenu dopo 3 secondi

    def draw(self):
        if self.show_loading:
            self.loading_screen.draw()  # Mostra la schermata di caricamento se necessario
        elif self.current_screen:
            self.current_screen.draw()
        pygame.display.flip()

    def mostra_first_screen(self):
        """Mostra la schermata iniziale per un intervallo di tempo o fino all'interazione dell'utente."""
        start_time = pygame.time.get_ticks()
        first_screen_shown = False

        while not first_screen_shown:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
                    # Interrompi la visualizzazione della first screen se l'utente preme un tasto o clicca
                    first_screen_shown = True

            # Continua a mostrare la first screen fino al raggiungimento dell'intervallo di tempo o fino
            # all'interazione dell'utente
            if pygame.time.get_ticks() - start_time < 3000:  # 3000 millisecondi = 3 secondi
                self.first_screen.draw()
            else:
                first_screen_shown = True

            pygame.display.flip()
            self.clock.tick(60)

    def mostra_loading_screen(self, durata=3000):
        """Mostra la schermata di caricamento per un intervallo di tempo specificato."""
        start_time = pygame.time.get_ticks()

        while pygame.time.get_ticks() - start_time < durata:  # durata in millisecondi
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            self.loading_screen.draw()  # Assumendo che LoadingScreen abbia un metodo draw
            pygame.display.flip()
            self.clock.tick(60)

    def mostra_schermata_sconfitta(self):
        """Mostra la schermata di sconfitta per 3 secondi o fino alla pressione di ESC."""
        start_time = pygame.time.get_ticks()
        esc_pressed = False  # Flag per controllare se ESC è stato premuto

        while not esc_pressed and pygame.time.get_ticks() - start_time < 3000:  # 3000 millisecondi = 3 secondi
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        esc_pressed = True  # ESC è stato premuto, esce dal loop

            self.schermata_sconfitta.mostra()  # Assumendo che SchermataSconfitta abbia un metodo draw
            pygame.display.flip()
            self.clock.tick(60)

    def mostra_schermata_vittoria(self):
        """Mostra la schermata di sconfitta per 3 secondi o fino alla pressione di ESC."""
        start_time = pygame.time.get_ticks()
        esc_pressed = False  # Flag per controllare se ESC è stato premuto

        while not esc_pressed and pygame.time.get_ticks() - start_time < 3000:  # 3000 millisecondi = 3 secondi
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        esc_pressed = True  # ESC è stato premuto, esce dal loop

            self.schermata_vittoria.mostra()  # Assumendo che SchermataSconfitta abbia un metodo draw
            pygame.display.flip()
            self.clock.tick(60)

    def mostra_schermata_scelta(self):
        clock = pygame.time.Clock()
        finestra_scelta = FinestraScelta(self.screen)

        while True:
            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                risposta = finestra_scelta.gestisci_eventi([evento])
                if risposta:
                    print(risposta)  # Stampa la risposta per debug
                    return risposta  # Restituisce la risposta e termina la funzione

            self.screen.fill((0, 0, 0))  # Sfondo nero
            finestra_scelta.disegna()
            pygame.display.flip()
            clock.tick(60)

    def ciclo_progressione(self):
        """Gestisce il ciclo di gioco con progressione continua."""
        while self.gioco_in_corso and self.livello_attuale < len(self.livelli):
            risultato = self.livelli[self.livello_attuale].esegui()
            caduta_player = self.livelli[self.livello_attuale].giocatore.verifica_collisione_con_terreno()
            # print(caduta_player + ' ciao')
            if risultato == "vittoria":
                self.livello_attuale += 1
            elif risultato == "sconfitta" or caduta_player == "sconfitta":
                self.mostra_schermata_sconfitta()
                if not self.gioco_in_corso:  # Assicurati che 'gioco_in_corso' venga aggiornato correttamente nel
                    # metodo 'game_over'
                    break

    def ciclo_progressione_test(self):
        """Gestisce il ciclo di gioco con progressione continua."""
        while self.gioco_in_corso and self.livello_attuale < len(self.livelli):
            risultato = self.livelli[self.livello_attuale].esegui()
            caduta_player = self.livelli[self.livello_attuale].giocatore.verifica_collisione_con_terreno()
            # print(caduta_player + ' ciao')
            if risultato == "vittoria":
                self.livello_attuale += 1
            elif risultato == "sconfitta" or caduta_player == "sconfitta":
                self.mostra_schermata_sconfitta()
                if not self.gioco_in_corso:  # Assicurati che 'gioco_in_corso' venga aggiornato correttamente nel
                    # metodo 'game_over'
                    break

    def ciclo_progressione_da(self, livello_iniziale):
        """Gestisce il ciclo di gioco con progressione continua da un livello specificato."""
        if livello_iniziale < 0 or livello_iniziale >= len(self.livelli):
            print("Numero di livello iniziale non valido. Inizio dal primo livello.")
            livello_iniziale = 0  # Imposta al primo livello, tenendo conto dell'indice basato su 0

        self.livello_attuale = livello_iniziale

        while self.gioco_in_corso and self.livello_attuale < len(self.livelli):
            risultato = self.livelli[self.livello_attuale].esegui()
            caduta_player = self.livelli[self.livello_attuale].giocatore.verifica_collisione_con_terreno()

            if risultato == "vittoria":
                self.livello_attuale += 1
            elif risultato == "sconfitta" or caduta_player == "sconfitta":
                # Mostra la schermata di sconfitta o qualsiasi altra logica di gestione della sconfitta
                print("Hai perso! Ritorno al menu principale.")
                self.mostra_schermata_sconfitta()
                break  # Interrompe il ciclo, facendo uscire dal ciclo di progressione

        if self.livello_attuale >= len(self.livelli):
            print("Tutti i livelli sono stati completati!")
            self.mostra_schermata_vittoria()

        # Dopo la fine del ciclo, potresti voler ritornare al menu principale o gestire la fine del gioco
        self.reset_gioco()

        # Opzionalmente, potresti voler gestire cosa succede quando tutti i livelli sono stati completati
        if self.livello_attuale >= len(self.livelli):
            print("Tutti i livelli sono stati completati!")

    def run(self):
        self.mostra_first_screen()
        while True:
            self.toggle_fullscreen()
            self.handle_events()
            self.update()
            self.draw()
            modalita_selezionata = self.mostra_menu_principale()
            print(modalita_selezionata)


            if modalita_selezionata in ['MEDIO', 'FACILE', 'DIFFICILE']:
                self.mostra_loading_screen()
                if modalita_selezionata == 'MEDIO':
                    self.configurazione.modifica_modality('MEDIO')
                    self.ciclo_progressione()

                elif modalita_selezionata == 'FACILE':
                    self.configurazione.modifica_modality('FACILE')
                    index = self.configurazione.leggi_level_passed()

                    # Mostra la schermata di scelta e attendi la risposta
                    if self.configurazione.leggi_level_passed() == 0:
                        self.ciclo_progressione_da(0)
                    else:
                        choice = self.mostra_schermata_scelta()

                        if choice == 'ricomincia':
                            # Se l'utente sceglie di ricominciare, il gioco riparte dall'inizio
                            self.configurazione.replace_level_passed(0)
                            self.ciclo_progressione_da(0)

                        elif choice == 'continua':
                            # Se l'utente sceglie di continuare, il gioco riparte dall'ultimo livello superato
                            self.ciclo_progressione_da(index)

                elif modalita_selezionata == 'DIFFICILE':
                    self.configurazione.modifica_modality('DIFFICILE')
                    self.ciclo_progressione_test()

            self.reset_gioco()
            self.toggle_fullscreen()


if __name__ == "__main__":
    gioco = GameScreen()
    gioco.run()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
