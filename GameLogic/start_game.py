import pygame
import time
from GameLogic.LevelClass import Livello


def open_pygame_window():
    pygame.init()  # Inizializza tutti i moduli pygame importati
    # Ottiene la risoluzione dello schermo corrente
    infoObject = pygame.display.Info()
    screen_width = infoObject.current_w
    screen_height = infoObject.current_h
    screen = pygame.display.set_mode((screen_width - 50, screen_height - 50))
    pygame.display.set_caption('Finestra Pygame')  # Imposta il titolo della finestra

    # Creazione del livello
    livello1 = Livello("Livello 1", "sfondo.jpg", "colonna_sonora.mp3")

    # Imposta lo sfondo iniziale della finestra a bianco
    screen.fill((255, 255, 255))
    # Carica il font per il nome del livello
    font = pygame.font.Font(None, 36)
    text = font.render(livello1.nome, True, (0, 0, 0))
    text_rect = text.get_rect(center=(screen_width // 2, screen_height // 2))
    screen.blit(text, text_rect)
    pygame.display.flip()

    # Attendi 5 secondi prima di cambiare lo sfondo
    time.sleep(5)

    # Carica lo sfondo del livello
    sfondo = pygame.image.load(livello1.sfondo)
    sfondo = pygame.transform.scale(sfondo, (screen_width - 50, screen_height - 50))
    # Ciclo principale del gioco
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:  # Controlla se l'utente ha chiuso la finestra
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:  # Permette di uscire con il tasto ESC
                    running = False

        # Aggiorna il display di Pygame ad ogni iterazione del ciclo
        pygame.display.flip()

    pygame.quit()
