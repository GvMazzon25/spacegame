import pygame


class SchermataSconfitta:
    def __init__(self, schermo):
        self.originale_sfondo = pygame.image.load(
            'C:/Users/gvmaz/OneDrive/Desktop/IA/Progetti/Infinity_alpha/Immagini/Caleidoscopio1.jpg').convert()
        self.schermo = schermo
        self.aggiorna_sfondo()
        self.font = pygame.font.Font(None, 74)  # Scegli un font e una dimensione appropriati

    def aggiorna_sfondo(self):
        # Aggiorna il ridimensionamento dello sfondo in base alla dimensione corrente dello schermo
        self.sfondo = pygame.transform.scale(self.originale_sfondo,
                                             (self.schermo.get_width(), self.schermo.get_height()))

    def mostra(self):
        self.aggiorna_sfondo()  # Assicurati che lo sfondo sia aggiornato con le dimensioni correnti dello schermo

        testo = "Hai perso!"
        superficie_testo = self.font.render(testo, True, (255, 0, 0))  # Colore rosso per il testo
        posizione_testo = superficie_testo.get_rect(
            center=(self.schermo.get_width() / 2, self.schermo.get_height() / 2))

        self.schermo.blit(self.sfondo, (0, 0))
        self.schermo.blit(superficie_testo, posizione_testo)
        pygame.display.flip()  # Aggiorna il display per mostrare le modifiche

        pygame.time.wait(3000)