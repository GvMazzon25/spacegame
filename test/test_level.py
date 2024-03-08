import pygame
import sys
import random


class Gioco:
    def __init__(self):
        pygame.init()

        # Impostazioni della finestra
        self.LARGHEZZA, self.ALTEZZA = 800, 600
        self.schermo = pygame.display.set_mode((self.LARGHEZZA, self.ALTEZZA))
        pygame.display.set_caption("Gioco Platform Scorrimento Orizzontale")
        self.clock = pygame.time.Clock()

        # Colori
        self.NERO = (0, 0, 0)
        self.BLU = (0, 0, 255)
        self.VERDE = (0, 255, 0)
        self.ROSSO = (255, 0, 0)
        self.AZZURRO = (0, 255, 255)

        # Parametri configurabili
        self.VELOCITA_TERRENO = -5
        self.DISTANZA_ORIZZONTALE_MIN = 150
        self.DISTANZA_ORIZZONTALE_MAX = 300
        self.DIFFERENZA_ALTEZZA_MAX = 50  # Differenza massima di altezza tra due terreni adiacenti
        self.SALTO_MAX = 120  # Distanza massima di salto verticale del personaggio

        self.giocatore = Giocatore(self)
        self.terreno = Terreno(self)

    def esegui(self):
        while True:
            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif evento.type == pygame.KEYDOWN:
                    if evento.key == pygame.K_SPACE:
                        self.giocatore.salta()

            self.giocatore.aggiorna(self.terreno)
            self.terreno.aggiorna()

            for ostacolo in self.terreno.ostacoli:
                if self.giocatore.rect.colliderect(ostacolo.rect):
                    self.giocatore.game_over()

            # Gestione collisione con il portale
            if self.terreno.portale and self.giocatore.rect.colliderect(self.terreno.portale.rect):
                self.livello_superato()

            self.schermo.fill(self.NERO)
            self.terreno.disegna(self.schermo)
            self.giocatore.disegna(self.schermo)
            if self.terreno.portale:
                self.terreno.portale.disegna(self.schermo)

            pygame.display.flip()
            self.clock.tick(30)

    def livello_superato(self):
        font = pygame.font.Font(None, 74)
        testo = font.render("Livello superato", 1, (255, 255, 255))
        testo_pos = testo.get_rect(centerx=self.schermo.get_width() / 2, centery=self.schermo.get_height() / 2)
        self.schermo.fill(self.NERO)  # Pulisce lo schermo prima di disegnare il messaggio
        self.schermo.blit(testo, testo_pos)
        pygame.display.flip()
        pygame.time.wait(3000)  # Aspetta 3 secondi prima di terminare
        pygame.quit()
        sys.exit()


# Classe Giocatore
class Giocatore(pygame.sprite.Sprite):
    def __init__(self, gioco):
        super().__init__()
        self.gioco = gioco
        self.surf = pygame.Surface((50, 50))
        self.surf.fill(self.gioco.BLU)
        self.rect = self.surf.get_rect(center=(self.gioco.LARGHEZZA // 8, self.gioco.ALTEZZA - 150))
        self.velocita_y = 0
        self.salti_rimanenti = 2

    def aggiorna(self, terreno):
        self.velocita_y += 1
        self.rect.move_ip(0, self.velocita_y)
        self.verifica_collisione_con_terreno(terreno)

    def verifica_collisione_con_terreno(self, terreno):
        self.rect.y += 1
        collisioni = [porzione for porzione in terreno.porzioni if self.rect.colliderect(porzione)]
        if collisioni:
            self.rect.bottom = collisioni[0].top
            self.velocita_y = 0
            self.salti_rimanenti = 2
        else:
            if not any(self.rect.bottom <= porzione.bottom for porzione in terreno.porzioni):
                self.game_over()
        self.rect.y -= 1

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
    def __init__(self, gioco, x, y):
        super().__init__()
        self.gioco = gioco
        self.surf = pygame.Surface((20, 50))
        self.surf.fill(self.gioco.ROSSO)
        self.rect = self.surf.get_rect(center=(x, y))

    def disegna(self, superficie):
        superficie.blit(self.surf, self.rect)


class Portale(pygame.sprite.Sprite):
    def __init__(self, gioco, x, y):
        super().__init__()
        self.gioco = gioco
        self.surf = pygame.Surface((20, 100))
        self.surf.fill(self.gioco.AZZURRO)
        self.rect = self.surf.get_rect(center=(x, y))

    def disegna(self, superficie):
        superficie.blit(self.surf, self.rect)


# Classe Terreno
class Terreno:
    def __init__(self, gioco):
        self.gioco = gioco
        self.porzioni = []
        self.ostacoli = []
        self.ultima_altezza = self.gioco.ALTEZZA - 50
        self.genera_terreno_iniziale()
        self.portale = None
        self.num_porzione_per_portale = random.randint(5, 9)

    def genera_terreno_iniziale(self):
        larghezza_porz = random.randint(self.gioco.LARGHEZZA // 4, self.gioco.LARGHEZZA // 2)
        self.porzioni.append(pygame.Rect(0, self.ultima_altezza, larghezza_porz, 50))

    def genera_portale(self):
        porzione = self.porzioni[self.num_porzione_per_portale - 1]
        self.portale = Portale(self.gioco, porzione.right + self.gioco.DISTANZA_ORIZZONTALE_MIN, porzione.top - 50)

    def aggiorna(self):
        self.aggiungi_porzione_se_necessario()
        self.muovi_terreno_e_ostacoli()
        if not self.portale and len(self.porzioni) >= self.num_porzione_per_portale:
            self.genera_portale()

    def aggiungi_porzione_se_necessario(self):
        while not self.porzioni or self.porzioni[-1].right < self.gioco.LARGHEZZA - self.gioco.DISTANZA_ORIZZONTALE_MAX:
            distanza_da_ultimo = random.randint(self.gioco.DISTANZA_ORIZZONTALE_MIN, self.gioco.DISTANZA_ORIZZONTALE_MAX)
            nuova_altezza = self.calcola_nuova_altezza()
            larghezza_nuova_porz = random.randint(self.gioco.LARGHEZZA // 4, self.gioco.LARGHEZZA // 2)
            nuova_porzione = pygame.Rect(self.porzioni[-1].right + distanza_da_ultimo, nuova_altezza,
                                         larghezza_nuova_porz, 50)
            self.porzioni.append(nuova_porzione)
            self.genera_ostacolo_per_porzione(nuova_porzione)

    def calcola_nuova_altezza(self):
        variazione_altezza = random.randint(-self.gioco.DIFFERENZA_ALTEZZA_MAX * 2, self.gioco.DIFFERENZA_ALTEZZA_MAX * 2)
        nuova_altezza = max(min(self.ultima_altezza + variazione_altezza, self.gioco.ALTEZZA - 100), 100)
        self.ultima_altezza = nuova_altezza
        return nuova_altezza

    def genera_ostacolo_per_porzione(self, porzione):
        if random.choice([True, True, True, False]):
            posizione_ostacolo = random.choice(['sinistra', 'centro', 'destra'])
            x_ostacolo = porzione.x + porzione.width * (0.25 if posizione_ostacolo == 'sinistra' else 0.5 if posizione_ostacolo == 'centro' else 0.75)
            self.ostacoli.append(Ostacolo(self.gioco, x_ostacolo, porzione.top - 25))

    def muovi_terreno_e_ostacoli(self):
        for porzione in self.porzioni:
            porzione.x += self.gioco.VELOCITA_TERRENO
        for ostacolo in self.ostacoli:
            ostacolo.rect.x += self.gioco.VELOCITA_TERRENO
        self.porzioni = [porzione for porzione in self.porzioni if porzione.right > 0]
        self.ostacoli = [ostacolo for ostacolo in self.ostacoli if ostacolo.rect.right > 0]

    def disegna(self, superficie):
        for porzione in self.porzioni:
            pygame.draw.rect(superficie, self.gioco.VERDE, porzione)
        for ostacolo in self.ostacoli:
            ostacolo.disegna(superficie)
        if self.portale:
            self.portale.disegna(superficie)


if __name__ == "__main__":
    gioco = Gioco()
    gioco.esegui()