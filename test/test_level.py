import pygame
import sys
import random

pygame.init()

LARGHEZZA, ALTEZZA = 800, 600
schermo = pygame.display.set_mode((LARGHEZZA, ALTEZZA))
pygame.display.set_caption("Gioco Platform Scorrimento Orizzontale")
clock = pygame.time.Clock()

# Colori
NERO = (0, 0, 0)
BLU = (0, 0, 255)
VERDE = (0, 255, 0)
ROSSO = (255, 0, 0)

# Parametri configurabili
VELOCITA_TERRENO = -5
DISTANZA_ORIZZONTALE_MIN = 150
DISTANZA_ORIZZONTALE_MAX = 300
DIFFERENZA_ALTEZZA_MAX = 50  # Differenza massima di altezza tra due terreni adiacenti
SALTO_MAX = 120  # Distanza massima di salto verticale del personaggio


# Classe Giocatore
class Giocatore(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.surf = pygame.Surface((50, 50))
        self.surf.fill(BLU)
        self.rect = self.surf.get_rect(center=(LARGHEZZA // 8, ALTEZZA - 150))
        self.velocita_y = 0
        self.salti_rimanenti = 2

    def aggiorna(self, terreno):
        self.velocita_y += 1
        self.rect.move_ip(0, self.velocita_y)
        self.verifica_collisione_con_terreno(terreno)

    def verifica_collisione_con_terreno(self, terreno):
        for porzione in terreno.porzioni:
            if self.rect.colliderect(porzione):
                self.rect.bottom = porzione.top
                self.velocita_y = 0
                self.salti_rimanenti = 2
                break
        else:
            if self.rect.bottom >= ALTEZZA:
                self.game_over()

    def salta(self):
        if self.salti_rimanenti > 0:
            self.velocita_y = -20
            self.salti_rimanenti -= 1

    def disegna(self, superficie):
        superficie.blit(self.surf, self.rect)

    def game_over(self):
        print("Hai perso!")
        pygame.quit()
        sys.exit()


# Classe Ostacolo
class Ostacolo(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.surf = pygame.Surface((20, 50))
        self.surf.fill(ROSSO)
        self.rect = self.surf.get_rect(center=(x, y))

    def disegna(self, superficie):
        superficie.blit(self.surf, self.rect)


# Classe Terreno
class Terreno():
    def __init__(self):
        self.porzioni = []
        self.ostacoli = []
        self.ultima_altezza = ALTEZZA - 50
        self.genera_terreno_iniziale()

    def genera_terreno_iniziale(self):
        larghezza_porz = random.randint(LARGHEZZA // 4, LARGHEZZA // 2)
        self.porzioni.append(pygame.Rect(0, self.ultima_altezza, larghezza_porz, 50))

    def aggiorna(self):
        self.aggiungi_porzione_se_necessario()
        self.muovi_terreno_e_ostacoli()

    def aggiungi_porzione_se_necessario(self):
        while not self.porzioni or self.porzioni[-1].right < LARGHEZZA - DISTANZA_ORIZZONTALE_MAX:
            distanza_da_ultimo = random.randint(DISTANZA_ORIZZONTALE_MIN, DISTANZA_ORIZZONTALE_MAX)
            nuova_altezza = self.calcola_nuova_altezza()
            larghezza_nuova_porz = random.randint(LARGHEZZA // 4, LARGHEZZA // 2)
            nuova_porzione = pygame.Rect(self.porzioni[-1].right + distanza_da_ultimo, nuova_altezza,
                                         larghezza_nuova_porz, 50)
            self.porzioni.append(nuova_porzione)
            self.genera_ostacolo_per_porzione(nuova_porzione)

    def calcola_nuova_altezza(self):
        # Calcola una nuova altezza per la porzione di terreno entro il limite di salto
        variazione_altezza = random.randint(-DIFFERENZA_ALTEZZA_MAX, DIFFERENZA_ALTEZZA_MAX)
        nuova_altezza = max(min(self.ultima_altezza + variazione_altezza, ALTEZZA - 50), ALTEZZA - 50 - SALTO_MAX)
        self.ultima_altezza = nuova_altezza
        return nuova_altezza

    def genera_ostacolo_per_porzione(self, porzione):
        # Decidi casualmente se generare un ostacolo sulla porzione di terreno
        if random.choice([True, False]):
            posizione_ostacolo = random.choice(['sinistra', 'centro', 'destra'])
            if posizione_ostacolo == 'sinistra':
                x_ostacolo = porzione.x + porzione.width * 0.25
            elif posizione_ostacolo == 'centro':
                x_ostacolo = porzione.x + porzione.width * 0.5
            else:  # 'destra'
                x_ostacolo = porzione.x + porzione.width * 0.75
            self.ostacoli.append(Ostacolo(x_ostacolo, porzione.top - 25))

    def muovi_terreno_e_ostacoli(self):
        for porzione in self.porzioni:
            porzione.x += VELOCITA_TERRENO
        for ostacolo in self.ostacoli:
            ostacolo.rect.x += VELOCITA_TERRENO
        self.porzioni = [porzione for porzione in self.porzioni if porzione.right > 0]
        self.ostacoli = [ostacolo for ostacolo in self.ostacoli if ostacolo.rect.right > 0]

    def disegna(self, superficie):
        for porzione in self.porzioni:
            pygame.draw.rect(superficie, VERDE, porzione)
        for ostacolo in self.ostacoli:
            ostacolo.disegna(superficie)


giocatore = Giocatore()
terreno = Terreno()

while True:
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif evento.type == pygame.KEYDOWN:
            if evento.key == pygame.K_SPACE:
                giocatore.salta()

    giocatore.aggiorna(terreno)
    terreno.aggiorna()

    # Verifica collisione con gli ostacoli
    for ostacolo in terreno.ostacoli:
        if giocatore.rect.colliderect(ostacolo.rect):
            giocatore.game_over()

    schermo.fill(NERO)
    terreno.disegna(schermo)
    giocatore.disegna(schermo)

    pygame.display.flip()
    clock.tick(30)