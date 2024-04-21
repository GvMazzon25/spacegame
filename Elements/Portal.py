import pygame


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