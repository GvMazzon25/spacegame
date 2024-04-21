import pygame


class Worm(pygame.sprite.Sprite):
    position = - 30

    def __init__(self, x, y, color=None):
        super().__init__()
        if color is None:
            color = (0, 255, 0)  # Colore verde come default se non specificato
        self.color = color
        self.surf = pygame.Surface((20, 70), pygame.SRCALPHA)  # Dimensioni della superficie per la pillola allungata
        pygame.draw.ellipse(self.surf, self.color, self.surf.get_rect())  # Disegna una pillola allungata
        self.rect = self.surf.get_rect(center=(x, y))
        self.altezza_massima = 55

    def disegna(self, superficie):
        superficie.blit(self.surf, self.rect)

    def emergi(self, porzione):
        # Riduci la y per far "emergere" il worm
        if self.rect.top > porzione.top - self.altezza_massima:
            self.rect.y -= 3