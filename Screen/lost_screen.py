import sys

import pygame


class SchermataPerdita:
    def __init__(self, schermo, punteggio):
        self.schermo = schermo
        self.punteggio = punteggio
        self.font = pygame.font.SysFont(None, 48)
        self.font_punteggio = pygame.font.SysFont(None, 36)

    def mostra(self, timeout=2000):  # Timeout in millisecondi
        inizio_tempo = pygame.time.get_ticks()  # Tempo di inizio

        self.schermo.fill((0, 0, 0))  # Sfondo nero
        testo = self.font.render("Hai perso!", True, (255, 0, 0))
        testo_punteggio = self.font_punteggio.render(f"Punteggio: {self.punteggio}", True, (255, 255, 255))

        testo_rect = testo.get_rect(center=(self.schermo.get_width() / 2, self.schermo.get_height() / 2))
        testo_punteggio_rect = testo_punteggio.get_rect(
            center=(self.schermo.get_width() / 2, self.schermo.get_height() / 2 + 50))

        self.schermo.blit(testo, testo_rect)
        self.schermo.blit(testo_punteggio, testo_punteggio_rect)
        pygame.display.flip()

        # Attende l'input dell'utente o il timeout
        attesa = True
        while attesa:
            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if evento.type == pygame.KEYDOWN:
                    if evento.key == pygame.K_RETURN:  # Tasto Enter per continuare
                        attesa = False

            if pygame.time.get_ticks() - inizio_tempo > timeout:  # Verifica il timeout
                attesa = False
