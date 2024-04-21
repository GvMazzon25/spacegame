import math
import pygame
import sys
import random
from pygame.math import Vector2

# Definizione della classe BlackHole
class BlackHole(pygame.sprite.Sprite):
    def __init__(self, x, y, attrazione_raggio):
        super().__init__()
        self.image = pygame.Surface((50, 50), pygame.SRCALPHA)
        self.rect = self.image.get_rect(center=(x, y))
        self.color = (0, 0, 0)
        pygame.draw.circle(self.image, self.color, (25, 25), 25)
        self.attrazione_raggio = attrazione_raggio

    def disegna(self, superficie):
        superficie.blit(self.image, self.rect)

    def calcola_forza_attrazione(self, player_pos):
        distanza = Vector2(player_pos[0] - self.rect.centerx, player_pos[1] - self.rect.centery)
        distanza_norm = distanza.length()
        if distanza_norm < self.attrazione_raggio:
            # Calcolo della forza di attrazione secondo la legge di gravitazione universale
            G = 6.67430e-11  # Costante gravitazionale
            massa_buco_nero = 1.989e30  # Massa del buco nero (espresso in kg, esempio per un buco nero stellare)
            massa_player = 70  # Massa del giocatore (espresso in kg, valore arbitrario)
            forza_magnitudine = G * (massa_buco_nero * massa_player) / (distanza_norm ** 2)
            forza_direzione = distanza.normalize()
            forza = forza_direzione * forza_magnitudine
            return -forza  # Invertiamo la direzione della forza
        else:
            return Vector2(0, 0)

# Definizione della classe Giocatore
class Giocatore(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.surf = pygame.Surface((50, 50))
        self.rect = self.surf.get_rect(center=(0, 0))  # Posizione iniziale non definita
        self.velocita = Vector2(0, 0)
        self.accelerazione = Vector2(0, 0)
        self.salti_rimanenti = 2

    def cambia_colore(self, nuovo_colore):
        self.surf.fill(nuovo_colore)

    def aggiorna(self):
        self.accelerazione = Vector2(0, 0)  # Resetta l'accelerazione
        self.velocita += self.accelerazione  # Aggiorna la velocità
        self.rect.move_ip(self.velocita)  # Sposta il giocatore

    def salta(self):
        pass

    def disegna(self, superficie):
        superficie.blit(self.surf, self.rect)

# Funzione per generare casualmente la posizione del giocatore intorno al buco nero
def genera_posizione_giocatore_around_black_hole(black_hole):
    angolo = random.uniform(0, 2 * math.pi)
    raggio = random.uniform(50, 150)  # Distanza massima dal buco nero
    x = black_hole.rect.centerx + raggio * math.cos(angolo)
    y = black_hole.rect.centery + raggio * math.sin(angolo)
    return x, y

# Funzione principale del gioco
def main():
    pygame.init()

    larghezza, altezza = 800, 600
    finestra = pygame.display.set_mode((larghezza, altezza))
    clock = pygame.time.Clock()

    black_hole = BlackHole(larghezza // 2, altezza // 2, attrazione_raggio=200)
    player = Giocatore()
    player.rect.center = genera_posizione_giocatore_around_black_hole(black_hole)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        # Calcola la forza di attrazione
        player_pos = player.rect.center
        forza_attrazione = black_hole.calcola_forza_attrazione(player_pos)

        # Applica la forza di attrazione all'accelerazione del giocatore
        player.accelerazione += forza_attrazione

        # Aggiorna la velocità del giocatore in base all'accelerazione
        player.velocita += player.accelerazione

        # Limita la velocità massima del giocatore per evitare che diventi troppo veloce
        velocita_massima = 10
        if player.velocita.length_squared() > velocita_massima ** 2:
            player.velocita.scale_to_length(velocita_massima)

        # Aggiorna la posizione del giocatore
        player.rect.move_ip(player.velocita)

        # Calcola la distanza dal buco nero
        distanza_buco_nero = Vector2(black_hole.rect.centerx - player.rect.centerx, black_hole.rect.centery - player.rect.centery).length()

        # Se il giocatore è abbastanza vicino al buco nero, lo fermiamo
        if distanza_buco_nero < 5:
            player.velocita *= 0

        finestra.fill((255, 255, 255))
        black_hole.disegna(finestra)
        player.disegna(finestra)
        pygame.display.flip()
        clock.tick(60)

if __name__ == "__main__":
    main()
