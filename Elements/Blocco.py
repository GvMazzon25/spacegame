import pygame


class Blocco:
    def __init__(self, x, y, larghezza, altezza, colore):
        self.X = x
        self.Y = y
        self.larghezza = larghezza
        self.altezza = altezza
        self.colore = colore
        self.rect = pygame.Rect(x, y, larghezza, altezza)
        self.colore = colore
        self.solido = True  # Blocco solido che interagisce con il giocatore
        self.toccato = False

    def disegna(self, superficie):
        pygame.draw.rect(superficie, self.colore, self.rect)

    @property
    def x(self):
        return self.rect.x

    @x.setter
    def x(self, value):
        self.rect.x = value

    @property
    def y(self):
        return self.rect.y

    @y.setter
    def y(self, value):
        self.rect.y = value

    @property
    def left(self):
        return self.rect.left

    @property
    def right(self):
        return self.rect.right

    @property
    def top(self):
        return self.rect.top

    @property
    def bottom(self):
        return self.rect.bottom


class BloccoSpecial(Blocco):
    def __init__(self, x, y, larghezza, altezza):
        # Imposta un colore predefinito per la lava, ad esempio rosso acceso

        super().__init__(x, y, larghezza, altezza, colore=None)
        self.solido = False  # BloccoLava non è solido
        self.colore = None
        # Aggiungi qui eventuali altre inizializzazioni specifiche per BloccoLava

    # Se desideri sovrascrivere il metodo disegna per aggiungere effetti speciali (ad esempio, animazioni)
    def disegna(self, superficie):
        pass

    # Potresti voler aggiungere metodi specifici per la gestione delle interazioni con il giocatore
    def interagisci_con_giocatore(self, giocatore):
        # Logica per danneggiare o influenzare il giocatore quando tocca il blocco di lava
        pass


class BloccoSand(Blocco):
    def __init__(self, x, y, larghezza, altezza):
        # Imposta un colore predefinito per la lava, ad esempio rosso acceso

        super().__init__(x, y, larghezza, altezza, colore=None)
        self.solido = False  # BloccoLava non è solido
        self.colore = (255, 165, 0)
        # Aggiungi qui eventuali altre inizializzazioni specifiche per BloccoLava

    # Se desideri sovrascrivere il metodo disegna per aggiungere effetti speciali (ad esempio, animazioni)
    def disegna(self, superficie):
        pygame.draw.rect(superficie, self.colore, self.rect)

    # Potresti voler aggiungere metodi specifici per la gestione delle interazioni con il giocatore
    def interagisci_con_giocatore(self, giocatore):
        # Logica per danneggiare o influenzare il giocatore quando tocca il blocco di lava
        pass
