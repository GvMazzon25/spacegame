import sys
from Utility.configuration import Configurazione
import pygame


class Giocatore2(pygame.sprite.Sprite):
    def __init__(self, gioco, livello):
        super().__init__()
        self.gioco = gioco
        self.surf = pygame.Surface((50, 50))
        self.colore_corrente = self.surf.fill(self.gioco.SKIN)
        self.rect = self.surf.get_rect(center=(self.gioco.LARGHEZZA // 8, 150))
        self.livello = livello
        self.n_livello = livello.n_level
        self.velocita_y = 1  # Inizialmente statico
        self.salti_rimanenti = 2
        self.gravita = - 1  # Gravità inizialmente normale (positiva)
        self.config = Configurazione()

    def cambia_colore(self, nuovo_colore):
        self.colore_corrente = self.surf.fill(nuovo_colore)
        self.surf.fill(nuovo_colore)

    def inverti_gravita(self):
        self.gravita *= -1  # Cambia la gravità da positiva a negativa e viceversa

    def aggiorna(self):
        self.velocita_y += self.gravita
        self.rect.y += self.velocita_y

        # Gestisci la collisione con il terreno
        self.verifica_collisione_con_terreno()

        if self.gravita == -1:
            if self.rect.bottom < 0:
                print("Game over iniziato a causa della caduta verso l'alto.")
                self.livello.game_over()
                self.config.replace_score(self.livello.punteggio)
                return "game over"
        else:
            if self.rect.top > self.gioco.ALTEZZA:
                caduta = self.livello.game_over()
                self.config.replace_score(self.livello.punteggio)
                return caduta

    def verifica_collisione_con_terreno(self):
        # Movimento verso l'alto per verificare le collisioni, poiché la gravità è invertita
        if self.gravita == -1:
            self.rect.y -= 1

            collisioni = [porzione for porzione in self.livello.terreno.porzioni
                          if hasattr(porzione, 'rect') and porzione.rect.colliderect(self.rect)]

            for porzione in collisioni:
                # Collisione mentre si muove verso l'alto (tecnicamente cadendo verso il basso)
                if self.velocita_y < 0 and self.rect.top <= porzione.bottom:
                    self.rect.top = porzione.bottom
                    self.velocita_y = 0  # Ferma il movimento verso l'alto
                    self.salti_rimanenti = 2  # Resetta i salti rimanenti
                    print('Salti rimanenti aggiornati dopo la collisione verso l\'alto.')

                # Collisione mentre si muove verso il basso (saltando verso il basso)
                elif self.gravita < 0 and self.velocita_y < 0 and self.rect.top <= porzione.bottom:
                    self.rect.bottom = porzione.top
                    self.velocita_y = 0  # Ferma il movimento verso il basso
                    self.salti_rimanenti = 2  # Resetta i salti rimanenti
                    print('Salti rimanenti aggiornati dopo il salto verso il basso.')

            return "continua"
        else:
            self.rect.y += 1

            collisioni = [porzione for porzione in self.livello.terreno.porzioni_inferiori
                          if hasattr(porzione, 'rect') and porzione.rect.colliderect(self.rect)]

            for porzione in collisioni:
                if hasattr(porzione, 'solido'):
                    if porzione.solido:

                        if self.velocita_y > 0:
                            self.rect.bottom = porzione.top
                            self.velocita_y = 0
                            self.salti_rimanenti = 2

                        else:
                            self.rect.top = porzione.bottom
                            self.velocita_y = 1
                        return "continua"
                    elif not porzione.solido and self.n_livello == 2:
                        # Rallenta la caduta se il blocco non è solido e il livello è 2
                        if self.velocita_y > 0:
                            self.velocita_y = max(self.velocita_y / 2,
                                                  1)  # Assicurati che la velocità non sia mai 0 o negativa
                return "continua"

    def salta(self):
        if self.salti_rimanenti > 0:
            if self.gravita == -1:
                self.velocita_y = 20  # Spinta verso il basso
            else:
                self.velocita_y = -20  # Spinta verso l'alto

            self.salti_rimanenti -= 1

    def disegna(self, superficie):
        superficie.blit(self.surf, self.rect)

    def nascondi(self):
        """Nasconde il giocatore rendendo la sua superficie completamente trasparente."""
        self.surf = pygame.Surface((50, 50), pygame.SRCALPHA)  # Crea una superficie trasparente
        self.surf.fill((0, 0, 0, 0))  # Rendi la superficie completamente trasparente


class Giocatore(pygame.sprite.Sprite):
    def __init__(self, gioco, livello):
        super().__init__()
        self.gioco = gioco
        self.surf = pygame.Surface((50, 50))
        self.colore_corrente = self.surf.fill(self.gioco.SKIN)
        self.rect = self.surf.get_rect(center=(self.gioco.LARGHEZZA // 8, self.gioco.ALTEZZA - 150))
        self.livello = livello
        self.n_livello = livello.n_level
        self.velocita_y = 1
        self.salti_rimanenti = 2
        self.config = Configurazione()
        self.in_salita = False
        self.posizione_originale_x = None

    def cambia_colore(self, nuovo_colore):
        self.colore_corrente = self.surf.fill(nuovo_colore)
        self.surf.fill(nuovo_colore)

    def verifica_collisione_con_plant(self):
        if self.livello.n_level == 4:
            collisioni_plant = [plant for plant in self.livello.terreno.plants
                                if plant.rect.colliderect(self.rect)]
            if collisioni_plant:
                plant = collisioni_plant[0]
                height = plant.height  # Prendi la prima pianta con cui collidi
                if not self.in_salita:  # Se non è già in salita
                    self.in_salita = True
                    self.posizione_originale_x = self.rect.x
                    self.rect.x = plant.rect.x  # Allinea con la pianta
                    self.velocita_y = -25  # Imposta la velocità di salita
                # Aggiungi il controllo per fermare la salita all'altezza desiderata
                target_height = plant.rect.y - (height)  # Calcola l'altezza target
                if self.rect.y <= target_height:
                    self.velocita_y = 0  # Ferma la salita
                    self.in_salita = False  # Indica che la salita è terminata

    def aggiorna(self):
        if not self.in_salita:
            self.velocita_y += 1  # Simula la gravità
            self.rect.y += self.velocita_y  # Aggiorna la posizione verticale
            self.verifica_collisione_con_terreno()
        else:
            if self.rect.y > self.livello.terreno.plant.rect.top:
                self.salta()
                self.rect.y += self.velocita_y  # Continua a salire
                self.rect.x += self.livello.VELOCITA_TERRENO
            else:
                self.velocita_y += 1
                # Inizia il ritorno graduale alla posizione x originale
                if self.rect.x != self.posizione_originale_x:
                    # Interpola linearmente tra la posizione attuale e quella originale
                    ritorno_velocita = 10  # Regola questo valore per cambiare la velocità del ritorno
                    distanza = self.posizione_originale_x - self.rect.x
                    passo = ritorno_velocita if abs(distanza) > ritorno_velocita else distanza
                    self.rect.x += passo
                else:
                    self.in_salita = False  # Termina la salita

    def verifica_collisione_con_terreno(self):
        self.rect.y += 1  # Piccolo spostamento verso il basso per verificare le collisioni
        collisioni = [porzione for porzione in self.livello.terreno.porzioni
                      if hasattr(porzione, 'rect') and porzione.rect.colliderect(self.rect)]

        for porzione in collisioni:
            if hasattr(porzione, 'solido'):
                if porzione.solido:

                    if self.velocita_y > 0:
                        self.rect.bottom = porzione.top
                        self.velocita_y = 0
                        self.salti_rimanenti = 2

                    else:
                        self.rect.top = porzione.bottom
                        self.velocita_y = 1
                    return "continua"
                elif not porzione.solido and self.n_livello == 2:
                    # Rallenta la caduta se il blocco non è solido e il livello è 2
                    if self.velocita_y > 0:
                        self.velocita_y = max(self.velocita_y / 2,
                                              1)  # Assicurati che la velocità non sia mai 0 o negativa
                    return "continua"

        if self.rect.top > self.gioco.ALTEZZA:
            caduta = self.livello.game_over()
            self.config.replace_score(self.livello.punteggio)
            return caduta
        return "continua"

    def salta(self):
        if self.salti_rimanenti > 0:
            if self.n_livello == 0:
                self.velocita_y = -17
            else:
                self.velocita_y = -20

            self.salti_rimanenti -= 1

    def disegna(self, superficie):
        superficie.blit(self.surf, self.rect)

    def nascondi(self):
        """Nasconde il giocatore rendendo la sua superficie completamente trasparente."""
        self.surf = pygame.Surface((50, 50), pygame.SRCALPHA)  # Crea una superficie trasparente
        self.surf.fill((0, 0, 0, 0))  # Rendi la superficie completamente trasparente
