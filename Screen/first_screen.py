import pygame
import sys
#"

class FirstScreen:
    def __init__(self, screen):
        self.screen = screen
        self.original_bg_image = pygame.image.load('C:/Users/gvmaz/OneDrive/Desktop/IA/Progetti/Infinity_alpha/Immagini/Infinity.jpg')  # Carica l'immagine originale
        self.bg_image = self.scale_bg_image(self.screen.get_size())  # Ridimensiona l'immagine allo schermo iniziale
        self.font = pygame.font.Font(None, 48)
        self.text = self.font.render("The Impossible Game", True, (0, 255, 255, 255))
        self.text_rect = self.text.get_rect(center=(self.screen.get_width() / 2, self.screen.get_height() / 2))

    def scale_bg_image(self, size):
        """Ridimensiona l'immagine di sfondo alle dimensioni specificate."""
        return pygame.transform.scale(self.original_bg_image, size)

    def draw(self):
        self.bg_image = self.scale_bg_image(self.screen.get_size())  # Ridimensiona l'immagine di sfondo
        self.screen.blit(self.bg_image, (0, 0))

        # Aggiorna la posizione del testo per centrarlo orizzontalmente e spostarlo più in basso verticalmente
        self.text_rect.center = (
        self.screen.get_width() / 2, self.screen.get_height() * 0.65)  # Sposta il testo più in basso
        self.screen.blit(self.text, self.text_rect)

        pygame.display.flip()