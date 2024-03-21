import sys

import pygame

from Utility.Exceptions import PerditaException


class Giocatore(pygame.sprite.Sprite):
    def __init__(self, gioco, livello):
        super().__init__()
        self.gioco = gioco
        self.surf = pygame.Surface((50, 50))
        self.colore_corrente = self.surf.fill(self.gioco.SKIN)
        self.rect = self.surf.get_rect(center=(self.gioco.LARGHEZZA // 8, self.gioco.ALTEZZA - 150))
        self.livello = livello
        self.velocita_y = 1
        self.salti_rimanenti = 2

    def cambia_colore(self, nuovo_colore):
        self.colore_corrente = self.surf.fill(nuovo_colore)
        self.surf.fill(nuovo_colore)

    def aggiorna(self):
        self.velocita_y += 1  # Simula la gravità
        self.rect.y += self.velocita_y  # Aggiorna la posizione verticale

        # Verifica collisione con il terreno e aggiorna di conseguenza
        self.verifica_collisione_con_terreno()

    def verifica_collisione_con_terreno(self):
        self.rect.y += 1  # Piccolo spostamento verso il basso per facilitare la verifica delle collisioni
        collisioni = [porzione for porzione in self.gioco.terreno.porzioni if self.rect.colliderect(porzione)]

        if collisioni:
            # Verifica se il giocatore sta cadendo (movimento verso il basso)
            if self.velocita_y > 0:
                self.rect.bottom = collisioni[0].top  # Collisione con il lato superiore
                self.velocita_y = 0
                self.salti_rimanenti = 2
            else:  # il giocatore si muove verso l'alto, quindi potrebbe collidere con il lato inferiore del terreno
                self.rect.top = collisioni[0].bottom  # Collisione con il lato inferiore
                self.velocita_y = 1  # Imposta una piccola velocità verso il basso per simulare il rimbalzo o la caduta

        else:
            # Se non ci sono collisioni e il giocatore è sotto un certo limite, ha perso
            if self.rect.top > self.gioco.ALTEZZA:
                game_over(self.livello)

        self.rect.y -= 1  # Ripristina la posizione originale se non c'è stata collisione

    def salta(self):
        if self.salti_rimanenti > 0:
            self.velocita_y = -20
            self.salti_rimanenti -= 1

    def disegna(self, superficie):
        superficie.blit(self.surf, self.rect)

    def vittoria(self):
        print("Hai vinto!")
        pygame.quit()
        sys.exit()


def game_over(livello):
    print("Hai perso!")
    score = livello.obtain_score()
    print(score)
    raise PerditaException(score)
