class PerditaException(Exception):
    def __init__(self, punteggio):
        super().__init__("Hai perso!")
        self.punteggio = punteggio
