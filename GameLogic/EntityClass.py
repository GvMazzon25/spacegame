class Entity:
    def __init__(self):
        self.vita = None
        self.gravita = None
        self.skin = None
        self.posizione_x = 0
        self.posizione_y = 0

    def muovi_su(self, distanza):
        self.posizione_y += distanza

    def muovi_giu(self, distanza):
        self.posizione_y -= distanza

    def muovi_destra(self, distanza):
        self.posizione_x += distanza

    def muovi_sinistra(self, distanza):
        self.posizione_x -= distanza


class Nemico(Entity):
    def __init__(self, nome, tipo):
        super().__init__()
        self.nome = nome
        self.tipo = tipo