from Levels.a_level_black import Livello0
from Levels.b_level_red import Livello1
import pygame
import sys


# Supponiamo che tu abbia già definito Livello0 e Livello1 come classi simili a quella che hai mostrato

class GestoreLivelli:
    def __init__(self):
        self.schermo = pygame.display.set_mode((800, 600))
        pygame.display.set_caption("Infinity")
        self.livelli = [Livello0(self.schermo), Livello1(self.schermo)]
        self.livello_attuale = 0

    def esegui(self):
        while self.livello_attuale < len(self.livelli):
            livello = self.livelli[self.livello_attuale]
            completato = livello.esegui()  # Esegui ritorna True quando il livello è completato
            if completato:
                self.livello_attuale += 1

        # Quando tutti i livelli sono completati, potresti mostrare una schermata finale o semplicemente uscire
        print("Tutti i livelli completati!")
        pygame.quit()
        sys.exit()


if __name__ == "__main__":
    gestore = GestoreLivelli()
    gestore.esegui()


