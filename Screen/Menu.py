import pygame
import sys

class MainMenu:
    def __init__(self, screen):
        self.screen = screen
        self.bg_image = pygame.image.load("C:/Users/gvmaz/OneDrive/Desktop/IA/Progetti/Infinity_alpha/Immagini/Caleidoscopio1.jpg")
        self.buttons = ["Difficile", "Medio", "Facile"]
        self.exit_button_text = "Exit"
        self.font = pygame.font.Font(None, 48)
        self.button_rects = []

    def scale_bg_image(self, size):
        """Ridimensiona l'immagine di sfondo alle dimensioni specificate."""
        return pygame.transform.scale(self.bg_image, size)

    def update_size(self, new_size):
        """Aggiorna le dimensioni e le posizioni dei componenti del menu."""
        # Aggiorna la dimensione della schermata
        self.screen = pygame.display.set_mode(new_size)
        # Ricarica e ridimensiona l'immagine di sfondo per adattarla alle nuove dimensioni
        self.bg_image = self.scale_bg_image(new_size)

        # Ricalcola la posizione dei bottoni e del pulsante Exit
        self.draw()

    def draw(self):
        bg_image_scaled = self.scale_bg_image(self.screen.get_size())
        self.screen.blit(bg_image_scaled, (0, 0))

        # Calcola posizione e disegna i bottoni per le modalità di gioco
        self.button_rects = []
        button_height = 50
        button_width = 200
        gap = 10
        total_height = (button_height + gap) * len(self.buttons) - gap
        start_y = (self.screen.get_height() - total_height) / 2

        for index, button_text in enumerate(self.buttons):
            button_x = (self.screen.get_width() - button_width) / 2
            button_y = start_y + (button_height + gap) * index
            button_rect = pygame.Rect(button_x, button_y, button_width, button_height)
            self.button_rects.append(button_rect)
            pygame.draw.rect(self.screen, (0, 255, 255), button_rect)
            text_surf = self.font.render(button_text, True, (255, 255, 255))
            text_rect = text_surf.get_rect(center=button_rect.center)
            self.screen.blit(text_surf, text_rect)

        # Pulsante Exit in alto a destra (dimensioni ridotte)
        exit_button_width = 80  # Dimensione ridotta
        exit_button_height = 30  # Dimensione ridotta
        exit_button_x = self.screen.get_width() - exit_button_width - gap
        exit_button_y = gap
        exit_button_rect = pygame.Rect(exit_button_x, exit_button_y, exit_button_width, exit_button_height)
        pygame.draw.rect(self.screen, (255, 0, 0), exit_button_rect)  # Rosso per il bottone "Exit"
        exit_text_surf = self.font.render(self.exit_button_text, True, (255, 255, 255))  # Bianco per il testo
        exit_text_rect = exit_text_surf.get_rect(center=exit_button_rect.center)
        self.screen.blit(exit_text_surf, exit_text_rect)

        pygame.display.flip()
        self.exit_button_rect = exit_button_rect  # Memorizza il rettangolo del pulsante Exit per il controllo del click

    def handle_click(self, pos):
        if self.exit_button_rect.collidepoint(pos):
            pygame.quit()
            sys.exit()
        for index, rect in enumerate(self.button_rects):
            if rect.collidepoint(pos):
                print(f"Button {self.buttons[index]} clicked, returning {index + 1}")
                return index + 1
        return 0