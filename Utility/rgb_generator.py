import random

def genera_colore_casuale():
    # Genera e ritorna una sequenza RGB casuale
    colore_rgb_casuale = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
    return colore_rgb_casuale
# Chiamata alla funzione per ottenere un colore casuale


if __name__ == '__main__':
    colore_casuale = genera_colore_casuale()
    print(colore_casuale)