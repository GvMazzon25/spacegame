import math

import pygame
from pygame import Vector2


class BlackHole(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.core_radius = 20
        self.event_horizon_radius = 2.3 * self.core_radius

        # Creazione delle componenti interne con la posizione iniziale
        self.singularity = Singularity(x, y, self.core_radius)
        self.event_horizon = EventHorizon(x, y, self.event_horizon_radius)

        # Questa superficie/rettangolo rappresenta l'area totale di BlackHole, ma non sarà disegnata direttamente.
        self.image = pygame.Surface((2 * self.event_horizon_radius, 2 * self.event_horizon_radius), pygame.SRCALPHA)
        self.rect = self.image.get_rect(center=(x, y))

    def update_position(self, dx):
        # Aggiorna la posizione di BlackHole e delle sue componenti
        self.rect.x += dx
        new_center = self.rect.center
        self.singularity.update_position(*new_center)
        self.event_horizon.update_position(*new_center)

    def disegna(self, surface):
        # Disegna l'Event Horizon e la Singularity sullo schermo.
        self.event_horizon.disegna(surface)
        self.singularity.disegna(surface)

    def inizia_animazione_event_horizon(self, screen, clock, disegna_sfondo):
        # Chiama il metodo per iniziare l'animazione su EventHorizon
        self.event_horizon.esegui_animazione(screen, clock, disegna_sfondo)


class Singularity(pygame.sprite.Sprite):
    def __init__(self, x, y, radius):
        super().__init__()
        self.radius = radius
        self.image = pygame.Surface((2 * radius, 2 * radius), pygame.SRCALPHA)
        self.rect = self.image.get_rect(center=(x-2, y-2))
        pygame.draw.circle(self.image, (0, 0, 0), (radius, radius), radius)

    def update_position(self, x, y):
        # Aggiorna la posizione del rettangolo di collisione
        self.rect.center = (x, y)

    def disegna(self, surface):
        # Disegna la singularity
        surface.blit(self.image, self.rect.topleft)


class EventHorizon(pygame.sprite.Sprite):
    def __init__(self, x, y, radius):
        super().__init__()
        self.radius = radius
        self.image_original = pygame.Surface((2 * radius, 2 * radius), pygame.SRCALPHA)
        self.rect = self.image_original.get_rect(center=(x, y))
        pygame.draw.circle(self.image_original, (255, 255, 255), (self.radius, self.radius), self.radius, 1)
        self.image = self.image_original.copy()

    def update_position(self, x, y):
        self.rect.center = (x, y)

    def disegna(self, surface):
        surface.blit(self.image, self.rect.topleft)

    def esegui_animazione(self, screen, clock, disegna_sfondo_callback):
        angle = 0
        while angle < 360:
            angle += 6  # Velocità dell'animazione, regola questo valore come necessario
            self.image = self.image_original.copy()
            end_x = int(self.radius + self.radius * math.cos(math.radians(angle)))
            end_y = int(self.radius + self.radius * math.sin(math.radians(angle)))
            pygame.draw.line(self.image, (255, 255, 0), (self.radius, self.radius), (end_x, end_y), 2)
            pygame.draw.arc(self.image, (255, 255, 0), (0, 0, 2 * self.radius, 2 * self.radius), 0, math.radians(angle),
                            2)

            # Chiama la funzione di callback per ridisegnare lo sfondo
            disegna_sfondo_callback()

            # Ora disegna l'EventHorizon sopra lo sfondo
            self.disegna(screen)
            pygame.display.flip()

            clock.tick(30)  # Mantiene l'animazione a una velocità costante
