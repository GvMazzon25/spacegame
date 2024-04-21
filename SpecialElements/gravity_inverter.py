import pygame


class GravityInverter(pygame.sprite.Sprite):
    def __init__(self, x, y, color=(0, 0, 255)):  # Blu come colore predefinito per l'inversione della gravità
        super().__init__()
        self.color = color
        self.width, self.height = 60, 60  # Dimensioni quadrate per rappresentare l'inversione
        self.image = pygame.Surface((self.width, self.height), pygame.SRCALPHA)  # Superficie trasparente
        self.draw_upward_arrow(self.image, self.color)  # Disegna una freccia verso l'alto
        self.rect = self.image.get_rect(center=(x, y))

    def draw_upward_arrow(self, surface, color):
        # Disegna una freccia che punta verso l'alto
        pygame.draw.polygon(surface, color, [
            (self.width / 2, 0),  # Punta della freccia in alto al centro
            (self.width * 0.25, self.height - self.width / 3),  # Leggermente a sinistra dalla base
            (0, self.height - self.width / 3),  # Angolo sinistro alla base
            (self.width / 2, self.height / 3),  # Centro verso l'alto interno
            (self.width, self.height - self.width / 3),  # Angolo destro alla base
            (self.width * 0.75, self.height - self.width / 3)  # Leggermente a destra dalla base
        ])

    def disegna(self, superficie):
        superficie.blit(self.image, self.rect.topleft)