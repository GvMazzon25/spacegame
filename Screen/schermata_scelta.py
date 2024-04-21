import pygame
from Utility.configuration import Configurazione

class FinestraScelta:
    def __init__(self, screen):
        self.screen = screen
        self.configurazione = Configurazione()
        # Ottiene le dimensioni dello schermo corrente
        schermo_dimensioni = screen.get_size()

        # Usa le dimensioni dello schermo per definire le dimensioni dello sfondo della finestra di scelta
        self.sfondo_dimensioni = schermo_dimensioni
        self.sfondo = pygame.Surface(self.sfondo_dimensioni).convert_alpha()
        self.sfondo.fill((100, 100, 100, 128))  # Grigio chiaro semi-trasparente per lo sfondo

        # Carica e ridimensiona un'immagine di sfondo per adattarla alle dimensioni dello schermo
        self.sfondo_immagine = pygame.image.load("C:/Users/gvmaz/OneDrive/Desktop/IA/Progetti/Infinity_alpha/Immagini/Caleidoscopio1.jpg").convert()
        self.sfondo_immagine = pygame.transform.scale(self.sfondo_immagine, schermo_dimensioni)

        self.font = pygame.font.SysFont(None, 40)
        self.colore_testo = (255, 255, 255)  # Bianco

        # Posiziona i pulsanti "Continua" e "Ricomincia" al centro dello schermo con uno spazio tra di loro
        spazio_centrale = 20  # Spazio centrale tra i pulsanti
        button_width = 200
        button_height = 50

        centro_x, centro_y = schermo_dimensioni[0] // 2, schermo_dimensioni[1] // 2

        # Pulsante "Continua"
        self.testo_continua = self.font.render("Continua", True, self.colore_testo)
        self.testo_continua_rect = self.testo_continua.get_rect(
            center=(centro_x - button_width // 2 - spazio_centrale // 2, centro_y))

        # Pulsante "Ricomincia"
        self.testo_ricomincia = self.font.render("Ricomincia", True, self.colore_testo)
        self.testo_ricomincia_rect = self.testo_ricomincia.get_rect(
            center=(centro_x + button_width // 2 + spazio_centrale // 2, centro_y))

    def disegna(self):
        # Disegna l'immagine di sfondo su tutta la schermata
        self.screen.blit(self.sfondo_immagine, (0, 0))
        # Applica uno sfondo semi-trasparente per aumentare il contrasto
        self.screen.blit(self.sfondo, (0, 0))

        # Disegna i pulsanti "Continua" e "Ricomincia"
        self.screen.blit(self.testo_continua, self.testo_continua_rect)
        self.screen.blit(self.testo_ricomincia, self.testo_ricomincia_rect)

    def gestisci_eventi(self, eventi):
        for evento in eventi:
            if evento.type == pygame.MOUSEBUTTONDOWN:
                # Controlla se il click è sui pulsanti
                if self.testo_continua_rect.collidepoint(evento.pos):
                    return "continua"
                elif self.testo_ricomincia_rect.collidepoint(evento.pos):
                    self.configurazione.reset_level_passed()
                    return "ricomincia"
        return None