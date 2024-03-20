from Levels.Level import Livello
import pygame
import sys
from Utility.configuration import Configurazione
from Utility.Exceptions import PerditaException
from Screen.lost_screen import SchermataPerdita
from Screen.Menu import MenuPrincipale


class GestoreLivelli:
    def __init__(self):
        pygame.init()
        self.schermo = pygame.display.set_mode((800, 600))
        pygame.display.set_caption("Infinity")

        # Crea un'istanza della classe Configurazione
        self.configurazione = Configurazione()

        # Usa il metodo ottieni_configurazione per ottenere le configurazioni specifiche
        config_livello_0 = self.configurazione.ottieni_configurazione(0)
        config_livello_1 = self.configurazione.ottieni_configurazione(1)

        # Crea i livelli usando le configurazioni ottenute
        self.livelli = [
            Livello(self.schermo, config_livello_0),
            Livello(self.schermo, config_livello_1)
        ]

        self.livello_attuale = 0

    def mostra_schermata_perdita(self, punteggio):
        # Crea e mostra la schermata di perdita passando il punteggio come argomento
        schermata_perdita = SchermataPerdita(self.schermo, punteggio)
        schermata_perdita.mostra()

    def mostra_menu_principale(self):
        # Mostra il menu principale e gestisce la selezione dell'utente
        menu = MenuPrincipale(self.schermo)
        menu.mostra()

    def esegui(self):
        while self.livello_attuale < len(self.livelli):
            livello_corrente = self.livelli[self.livello_attuale]
            try:
                completato = livello_corrente.esegui()
                if completato:
                    self.livello_attuale += 1
                    # Puoi passare informazioni tra livelli qui se necessario
            except PerditaException as e:
                punteggio = e.punteggio
                self.mostra_schermata_perdita(punteggio)
                # Gestisci la perdita qui
                self.mostra_schermata_perdita(punteggio)
                self.mostra_menu_principale()
                self.livello_attuale = 0  # Ricomincia dal primo livello
                break  # Esci dal ciclo di gioco principale


if __name__ == "__main__":
    while True:
        gestore = GestoreLivelli()
        gestore.mostra_menu_principale()
        gestore.esegui()
