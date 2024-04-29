import pygame


class Plant(pygame.sprite.Sprite):
    position = - 30

    def __init__(self, x, y, height, color=None):
        super().__init__()
        if color is None:
            color = (0, 255, 0)  # Colore verde come default se non specificato
        self.color = color
        self.height = height
        self.surf = pygame.Surface((10, self.height), pygame.SRCALPHA)  # Dimensioni della superficie per la pillola
        # allungata
        pygame.draw.ellipse(self.surf, self.color, self.surf.get_rect())  # Disegna una pillola allungata
        self.rect = self.surf.get_rect(center=(x, y + 300))

    def disegna(self, superficie):
        superficie.blit(self.surf, self.rect)

