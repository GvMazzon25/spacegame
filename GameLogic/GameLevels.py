import pygame
import time

class Game:
    def __init__(self, livelli):
        self.livelli = livelli

    def apri_finestra(self):
        pygame.init()
        infoObject = pygame.display.Info()
        screen_width = infoObject.current_w
        screen_height = infoObject.current_h
        screen = pygame.display.set_mode((screen_width - 50, screen_height - 50))
        pygame.display.set_caption('Finestra Pygame')

        clock = pygame.time.Clock()

        for livello in self.livelli:
            # Schermata bianca con il nome del livello
            screen.fill((255, 255, 255))
            font = pygame.font.Font(None, 36)
            text = font.render(livello.nome, True, (0, 0, 0))
            text_rect = text.get_rect(center=(screen_width // 2, screen_height // 2))
            screen.blit(text, text_rect)
            pygame.display.flip()

            # Attendi 5 secondi prima di visualizzare lo sfondo del livello
            time.sleep(5)

            # Carica lo sfondo del livello
            sfondo = pygame.image.load(livello.sfondo)
            sfondo = pygame.transform.scale(sfondo, (screen_width - 50, screen_height - 50))
            screen.blit(sfondo, (0, 0))
            pygame.display.flip()

            # Attendi 5 secondi prima di passare al prossimo livello
            time.sleep(5)

        # Chiudi la finestra quando tutti i livelli sono stati visualizzati
        pygame.quit()

