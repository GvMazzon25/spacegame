import sys
import pygame


class MenuPrincipale:
    def __init__(self, schermo):
        self.schermo = schermo
        self.font = pygame.font.SysFont(None, 48)
        self.bottone_colore = (0, 255, 0)  # Colore verde per il bottone
        self.testo_colore = (255, 255, 255)  # Colore bianco per il testo

        # Crea i rettangoli per i bottoni
        larghezza_bottone = 200
        altezza_bottone = 50
        spazio_tra_bottoni = 20
        totale_altezza = 3 * altezza_bottone + 2 * spazio_tra_bottoni
        inizio_y = self.schermo.get_height() / 2 - totale_altezza / 2

        self.bottoni = [
            pygame.Rect(self.schermo.get_width() / 2 - larghezza_bottone / 2, inizio_y, larghezza_bottone, altezza_bottone),
            pygame.Rect(self.schermo.get_width() / 2 - larghezza_bottone / 2, inizio_y + altezza_bottone + spazio_tra_bottoni, larghezza_bottone, altezza_bottone),
            pygame.Rect(self.schermo.get_width() / 2 - larghezza_bottone / 2, inizio_y + 2 * (altezza_bottone + spazio_tra_bottoni), larghezza_bottone, altezza_bottone)
        ]

        self.modalita_testi = ["DIFFICILE", "MEDIO", "FACILE"]

    def mostra(self):
        self.schermo.fill((0, 0, 0))  # Sfondo nero

        for bottone, modalita in zip(self.bottoni, self.modalita_testi):
            pygame.draw.rect(self.schermo, self.bottone_colore, bottone)
            testo = self.font.render(modalita, True, self.testo_colore)
            testo_rect = testo.get_rect(center=bottone.center)
            self.schermo.blit(testo, testo_rect)

        pygame.display.flip()

        modalita_selezionata = None
        attesa = True
        while attesa:
            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif evento.type == pygame.MOUSEBUTTONDOWN:
                    for i, bottone in enumerate(self.bottoni):
                        if bottone.collidepoint(evento.pos):
                            modalita_selezionata = self.modalita_testi[i]  # Assegna il testo della modalità
                            attesa = False
                            break

        return modalita_selezionata
