import pygame
import time
from GameLogic.LevelClass import Livello
from GameLogic.GameLevels import Game

sfondo1 = "C:/Users/gvmaz/OneDrive/Desktop/IA/Progetti/spacegame/Utility/Images/sfondo1.webp"
sfondo2 = "C:/Users/gvmaz/OneDrive/Desktop/IA/Progetti/spacegame/Utility/Images/sfondo2.webp"

def open_pygame_window():
    # Creazione dei livelli
    livelli = [
        Livello("Livello 1", sfondo1, "colonna_sonora1.mp3"),
        Livello("Livello 2", sfondo2, "colonna_sonora2.mp3"),
    ]

    # Creazione del gioco e apertura della finestra
    game = Game(livelli)
    game.apri_finestra()
