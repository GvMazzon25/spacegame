import sys

import pygame


class MenuPrincipale:
    def __init__(self, schermo):
        self.schermo = schermo
        self.font = pygame.font.SysFont(None, 48)
        self.bottone_colore = (0, 255, 0)  # Colore verde per il bottone
        self.testo_colore = (255, 255, 255)  # Colore bianco per il testo
        self.bottone = pygame.Rect(self.schermo.get_width() / 2 - 100, self.schermo.get_height() / 2 - 25, 200, 50)  # Posiziona e dimensiona il bottone

    def mostra(self):
        self.schermo.fill((0, 0, 0))  # Sfondo nero
        # Disegna il bottone
        pygame.draw.rect(self.schermo, self.bottone_colore, self.bottone)

        # Aggiungi il testo sul bottone
        testo = self.font.render("Start Game", True, self.testo_colore)
        testo_rect = testo.get_rect(center=self.bottone.center)
        self.schermo.blit(testo, testo_rect)
        pygame.display.flip()

        attesa = True
        while attesa:
            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif evento.type == pygame.MOUSEBUTTONDOWN:
                    # Controlla se il click è all'interno del rettangolo del bottone
                    if self.bottone.collidepoint(evento.pos):
                        attesa = False
                elif evento.type == pygame.KEYDOWN and evento.key == pygame.K_RETURN:
                    # Permetti anche di iniziare il gioco premendo ENTER
                    attesa = False

        return True  # Indica che il gioco può iniziare
