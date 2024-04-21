import pygame
import sys
import math

class LoadingScreen:
    def __init__(self, screen):
        self.screen = screen
        self.bg_image = pygame.image.load("C:/Users/gvmaz/OneDrive/Desktop/IA/Progetti/Infinity_alpha/Immagini/Caleidoscopio1.jpg")  # Sostituisci con il tuo sfondo
        self.colors = [
            (255, 0, 0),  # Rosso
            (255, 127, 0),  # Arancione
            (255, 255, 0),  # Giallo
            (0, 255, 0),  # Verde
            (0, 0, 255),  # Blu
            (75, 0, 130),  # Indaco
            (148, 0, 211)  # Violetto
        ]
        self.radius = 100  # Raggio della circonferenza su cui i pallini si muovono
        self.dot_radius = 25  # Raggio dei pallini
        self.angle = 0  # Angolo iniziale

    def draw(self):
        # Centra l'animazione
        center_x, center_y = self.screen.get_width() / 2, self.screen.get_height() / 2

        # Ridimensiona e disegna lo sfondo
        bg_image_scaled = pygame.transform.scale(self.bg_image, self.screen.get_size())
        self.screen.blit(bg_image_scaled, (0, 0))

        # Disegna i pallini
        for i, color in enumerate(self.colors):
            angle_rad = math.radians(self.angle + (i * 360 / len(self.colors)))
            x = center_x + math.cos(angle_rad) * self.radius
            y = center_y + math.sin(angle_rad) * self.radius
            pygame.draw.circle(self.screen, color, (int(x), int(y)), self.dot_radius)

        # Aggiorna l'angolo per la prossima iterazione (velocità dell'animazione)
        self.angle += 2
        if self.angle >= 360:
            self.angle -= 360

        pygame.display.flip()


