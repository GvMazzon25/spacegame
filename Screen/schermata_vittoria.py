import pygame


class SchermataVittoria:
    def __init__(self, schermo):
        self.schermo = schermo
        # Carica un'immagine di sfondo
        self.sfondo = pygame.image.load('C:/Users/gvmaz/OneDrive/Desktop/IA/Progetti/Infinity_alpha/Immagini/Caleidoscopio1.jpg').convert()
        self.sfondo = pygame.transform.scale(self.sfondo, (schermo.get_width(), schermo.get_height()))
        self.font = pygame.font.Font(None, 74)  # Scegli un font e una dimensione appropriati

    def mostra(self):
        # Centra il testo nella schermata
        testo = "Gioco superato!"
        superficie_testo = self.font.render(testo, True, (255, 0, 0))  # Colore rosso per il testo
        posizione_testo = superficie_testo.get_rect(center=(self.schermo.get_width() / 2, self.schermo.get_height() / 2))

        # Disegna lo sfondo e il testo
        self.schermo.blit(self.sfondo, (0, 0))
        self.schermo.blit(superficie_testo, posizione_testo)
        pygame.display.flip()  # Aggiorna il display per mostrare le modifiche

        # Mantiene la schermata visibile per 3 secondi prima di procedere
        pygame.time.wait(3000)