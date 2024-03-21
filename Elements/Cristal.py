import random
from Utility.rgb_generator import genera_colore_casuale as rgb_generator
import pygame


class Cristallo(pygame.sprite.Sprite):
    COLORI = [
        (255, 0, 0),  # Rosso
        (255, 165, 0),  # Arancione
        (255, 255, 0),  # Giallo
        (0, 128, 0),  # Verde
        (0, 0, 255),  # Blu
        (128, 0, 128),  # Viola
        (75, 0, 130)  # Indaco
    ]

    def __init__(self, x, y, color=None):
        super().__init__()
        # Se non viene specificato un colore, ne sceglie uno casualmente dalla lista COLORI
        self.color = color if color is not None else random.choice(Cristallo.COLORI)
        self.surf = pygame.Surface((20, 40), pygame.SRCALPHA)  # Dimensioni del rombo
        pygame.draw.polygon(self.surf, self.color, [(10, 0), (20, 20), (10, 40), (0, 20)])  # Disegna un rombo
        self.rect = self.surf.get_rect(center=(x, y))

    def disegna(self, superficie):
        superficie.blit(self.surf, self.rect)


class CristalloTest(pygame.sprite.Sprite):
    RAINBOW = [
        (255, 0, 0),  # Rosso
        (255, 165, 0),  # Arancione
        (255, 255, 0),  # Giallo
        (0, 128, 0),  # Verde
        (0, 0, 255),  # Blu
        (128, 0, 128),  # Viola
        (75, 0, 130)  # Indaco
    ]

    def __init__(self, x, y, colore_obbligatorio, use_random_color_generator=False):
        super().__init__()
        self.surf = pygame.Surface((20, 40), pygame.SRCALPHA)  # Dimensioni del rombo
        self.colore = colore_obbligatorio if not use_random_color_generator else rgb_generator()
        self.disegna_con_colore(x, y)

    def disegna_fixed_color(self, x, y):
        # Sceglie un colore dalla lista COLORI
        color = random.choice(Cristallo.RAINBOW)
        pygame.draw.polygon(self.surf, color, [(10, 0), (20, 20), (10, 40), (0, 20)])  # Disegna un rombo
        self.rect = self.surf.get_rect(center=(x, y))

    def disegna_random_color(self, x, y):
        # Usa la funzione rgb_generator per scegliere un colore
        color = rgb_generator()
        pygame.draw.polygon(self.surf, color, [(10, 0), (20, 20), (10, 40), (0, 20)])  # Disegna un rombo
        self.rect = self.surf.get_rect(center=(x, y))

    def disegna_con_colore(self, x, y):
        """Genera il cristallo con un colore specifico."""
        pygame.draw.polygon(self.surf, self.colore, [(10, 0), (20, 20), (10, 40), (0, 20)])  # Disegna un rombo
        self.rect = self.surf.get_rect(center=(x, y))

    # Metodo per disegnare il cristallo sulla superficie del gioco
    def disegna(self, superficie):
        superficie.blit(self.surf, self.rect)
