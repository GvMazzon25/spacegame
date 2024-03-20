import sys

import pygame


class MenuPrincipale:
    def __init__(self, schermo):
        self.schermo = schermo
        self.font = pygame.font.SysFont(None, 48)

    def mostra(self):
        self.schermo.fill((0, 0, 0))  # Sfondo nero
        testo = self.font.render("Premi ENTER per iniziare", True, (255, 255, 255))
        testo_rect = testo.get_rect(center=(self.schermo.get_width() / 2, self.schermo.get_height() / 2))
        self.schermo.blit(testo, testo_rect)
        pygame.display.flip()

        # Attende l'input dell'utente
        attesa = True
        while attesa:
            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if evento.type == pygame.KEYDOWN:
                    if evento.key == pygame.K_RETURN:  # Tasto Enter per iniziare
                        attesa = False
        return True  # Aggiungi il ritorno per indicare l'inizio del gioco
