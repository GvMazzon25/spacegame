import pygame


class Coin(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.surf = pygame.Surface((10, 10))  # Dimensioni del coin
        self.surf.fill((255, 255, 0))  # Colore giallo per il coin
        self.rect = self.surf.get_rect(center=(x, y))

    def disegna(self, superficie):
        superficie.blit(self.surf, self.rect)



class CoinManager:
    def __init__(self, gioco):
        self.gioco = gioco
        self.coins = pygame.sprite.Group()

    def genera_coins_tra_terreni(self, porzione_prec, porzione_succ):
        start_x = porzione_prec.right
        end_x = porzione_succ.left
        ground_y = max(porzione_prec.bottom, porzione_succ.bottom)
        peak_y = min(porzione_prec.top, porzione_succ.top) - 150  # Altezza del vertice della parabola
        num_coins = 15  # Numero di coin

        # Definiamo un offset per sollevare i punti di inizio e fine della parabola
        start_end_offset = 30  # Solleva di 20 pixel sopra la linea del terreno

        # Calcolo della larghezza della traiettoria parabolica e dell'altezza
        width = end_x - start_x
        height = peak_y - ground_y + start_end_offset

        for i in range(num_coins):
            # Normalizza la posizione dei coin lungo l'asse x
            normalized_x = (i / (num_coins - 1)) - 0.5  # -0.5 a 0.5
            # Calcola la posizione x del coin
            x = start_x + (i / (num_coins - 1)) * width
            # Calcola la posizione y del coin usando una formula parabolica semplice
            y = peak_y - 4 * height * (normalized_x ** 2) - start_end_offset

            self.coins.add(Coin(x, y))



class CoinManager:
    def __init__(self, gioco):
        self.gioco = gioco
        self.coins = pygame.sprite.Group()

    def genera_coins_tra_terreni(self, porzione_prec, porzione_succ):
        start_x = porzione_prec.right
        end_x = porzione_succ.left
        ground_y = max(porzione_prec.bottom, porzione_succ.bottom)
        peak_y = min(porzione_prec.top, porzione_succ.top) - 150  # Altezza del vertice della parabola
        num_coins = 15  # Numero di coin

        # Definiamo un offset per sollevare i punti di inizio e fine della parabola
        start_end_offset = 30  # Solleva di 20 pixel sopra la linea del terreno

        # Calcolo della larghezza della traiettoria parabolica e dell'altezza
        width = end_x - start_x
        height = peak_y - ground_y + start_end_offset

        for i in range(num_coins):
            # Normalizza la posizione dei coin lungo l'asse x
            normalized_x = (i / (num_coins - 1)) - 0.5  # -0.5 a 0.5
            # Calcola la posizione x del coin
            x = start_x + (i / (num_coins - 1)) * width
            # Calcola la posizione y del coin usando una formula parabolica semplice
            y = peak_y - 4 * height * (normalized_x ** 2) - start_end_offset

            self.coins.add(Coin(x, y))

    def aggiorna(self):
        # Muovi i coin insieme al terreno
        for coin in self.coins:
            coin.rect.x += self.gioco.VELOCITA_TERRENO
            # Se un coin esce dallo schermo, viene eliminato
            if coin.rect.right < 0:
                coin.kill()

    def gestisci_collisioni(self, giocatore):
        coins_colpiti = pygame.sprite.spritecollide(giocatore, self.coins, True)
        if coins_colpiti:
            self.gioco.punteggio += len(coins_colpiti)

    def disegna(self, superficie):
        for coin in self.coins:
            coin.disegna(superficie)

