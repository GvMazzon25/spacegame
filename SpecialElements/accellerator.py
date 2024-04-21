import random
import pygame


class Accelerator(pygame.sprite.Sprite):
    def __init__(self, x, y, color=(255, 255, 0)):  # Giallo come colore predefinito per l'accelerazione
        super().__init__()
        self.color = color
        self.width, self.height = 60, 30  # Dimensioni modificate per un orientamento orizzontale
        self.image = pygame.Surface((self.width, self.height), pygame.SRCALPHA)  # Superficie trasparente
        self.draw_horizontal_arrow(self.image, self.color)  # Disegna la freccia orizzontale sull'oggetto
        self.rect = self.image.get_rect(center=(x, y))

    def draw_horizontal_arrow(self, surface, color):
        # Disegna una freccia che punta verso sinistra
        pygame.draw.polygon(surface, color, [
            (self.width, self.height / 2),  # Punto medio sulla destra
            (self.height, 0),  # Angolo superiore dopo la punta, vicino alla base
            (self.height, self.height * 0.25),  # Leggermente giù dall'angolo superiore, vicino alla base
            (0, self.height / 2),  # Punta della freccia al centro a sinistra
            (self.height, self.height * 0.75),  # Leggermente su dall'angolo inferiore, vicino alla base
            (self.height, self.height),  # Angolo inferiore dopo la punta, vicino alla base
            (self.width, self.height / 2)  # Ritorna al punto medio sulla destra
        ])

    def disegna(self, superficie):
        superficie.blit(self.image, self.rect.topleft)
