from Levels.Level import Livello
import pygame
from Utility.configuration import Configurazione
from Utility.Exceptions import PerditaException
from Screen.lost_screen import SchermataPerdita
from Screen.Menu import MenuPrincipale


class GestoreLivelli:
    def __init__(self):
        pygame.init()
        self.schermo = pygame.display.set_mode((800, 600))
        pygame.display.set_caption("Infinity")
        self.configurazione = Configurazione()
        self.inizializza_gioco()

    def inizializza_gioco(self):
        """Inizializza o reinizializza lo stato del gioco per una nuova sessione."""
        self.livello_attuale = 0
        self.ultimo_livello_raggiunto = 0
        # Carica i livelli in base alla configurazione corrente
        self.livelli = [
            Livello(self.schermo, self.configurazione.ottieni_configurazione(0)),
            Livello(self.schermo, self.configurazione.ottieni_configurazione(1))
        ]

    def reset_gioco(self):
        """Resetta lo stato del gioco per una nuova sessione."""
        self.inizializza_gioco()

    def mostra_menu_principale(self):
        menu = MenuPrincipale(self.schermo)
        modalita_selezionata = menu.mostra()
        return modalita_selezionata

    def mostra_schermata_perdita(self, punteggio):
        schermata_perdita = SchermataPerdita(self.schermo, punteggio)
        decisione = schermata_perdita.mostra()
        return decisione

    def esegui(self):
        while True:
            self.reset_gioco()  # Assicurati di resettare il gioco prima di iniziare una nuova sessione
            modalita_selezionata = self.mostra_menu_principale()
            if modalita_selezionata == "MEDIO":
                self.esegui_ciclo_gioco_Medio()
            elif modalita_selezionata == "FACILE":
                self.esegui_ciclo_gioco_Facile(self.ultimo_livello_raggiunto)
            elif modalita_selezionata == "DIFFICILE":
                print("Modalità DIFFICILE selezionata - Funzionalità in fase di sviluppo.")

    def esegui_ciclo_gioco_Medio(self):
        while self.livello_attuale < len(self.livelli):
            livello_corrente = self.livelli[self.livello_attuale]
            try:
                completato = livello_corrente.esegui()
                if completato:
                    self.livello_attuale += 1
                    # Puoi passare informazioni tra livelli qui se necessario
            except PerditaException as e:
                print('ciao')
                punteggio = e.punteggio
                self.mostra_schermata_perdita(punteggio)
                # Gestisci la perdita qui
                self.mostra_schermata_perdita(punteggio)
                self.mostra_menu_principale()
                self.livello_attuale = 0  # Ricomincia dal primo livello
                break  # Esci dal ciclo di gioco principale
            continue

    def esegui_ciclo_gioco_Facile(self, ultimo_livello_raggiunto):
        self.livello_attuale = ultimo_livello_raggiunto
        while self.livello_attuale < len(self.livelli):
            try:
                livello_corrente = self.livelli[self.livello_attuale]
                completato = livello_corrente.esegui()
                if completato:
                    self.livello_attuale += 1
                    self.ultimo_livello_raggiunto = self.livello_attuale
            except PerditaException as e:
                uscire = self.mostra_schermata_perdita(e.punteggio)
                print(uscire)
                if uscire:
                    break  # Esci dal ciclo e potenzialmente torna al menu principale
                else:
                    # Potresti voler resettare lo stato del livello corrente qui
                    break
            print('ciao')


if __name__ == "__main__":
    gestore = GestoreLivelli()
    gestore.esegui()
    # Non creare una nuova istanza di GestoreLivelli, usa l'istanza esistente
