class Livello:
    def __init__(self, nome, sfondo, colonna_sonora):
        self.nome = nome
        self.sfondo = sfondo
        self.colonna_sonora = colonna_sonora
        self.nemici = []
        self.terreno = None

    def aggiungi_nemico(self, nemico):
        self.nemici.append(nemico)

    def imposta_terreno(self, terreno):
        self.terreno = terreno

class Nemico:
    def __init__(self, nome, tipo):
        self.nome = nome
        self.tipo = tipo

class Terreno:
    def __init__(self, tipo):
        self.tipo = tipo