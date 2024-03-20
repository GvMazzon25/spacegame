class Configurazione:
    def __init__(self):
        self.configurazioni = [
            {
                'SFONDO': (0, 0, 0),
                'SKIN': (0, 0, 255),
                'TERRENO': (0, 255, 0),
                'ROSSO': (255, 0, 0),
                'AZZURRO': (0, 255, 255),
                'VELOCITA_TERRENO': -8,
                'DISTANZA_ORIZZONTALE_MIN': 150,
                'DISTANZA_ORIZZONTALE_MAX': 300,
                'DIFFERENZA_ALTEZZA_MAX': 50,
                'SALTO_MAX': 100,
                'MAIN_COLOR': (255, 0, 0),
            },
            {
                'SFONDO': (255, 255, 255),
                'SKIN': (255, 165, 0),  # Arancione
                'TERRENO': (0, 255, 0),
                'ROSSO': (255, 0, 0),
                'AZZURRO': (0, 255, 255),
                'VELOCITA_TERRENO': -10,
                'DISTANZA_ORIZZONTALE_MIN': 200,
                'DISTANZA_ORIZZONTALE_MAX': 350,
                'DIFFERENZA_ALTEZZA_MAX': 60,
                'SALTO_MAX': 120,
                'MAIN_COLOR': (255, 165, 0),  # Arancione
            },
            # Aggiungi altre configurazioni qui...
        ]

    def ottieni_configurazione(self, numero):
        if 0 <= numero < len(self.configurazioni):
            return self.configurazioni[numero]
        else:
            raise IndexError("Numero di configurazione non valido.")