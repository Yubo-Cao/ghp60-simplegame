import pygame as pg

from .constants import SIZE, TITLE, ICON
from .endscreen import EndScreen
from .game import Game
from .menu import MainMenu


def main():
    pg.init()

    surface = pg.display.set_mode(SIZE, pg.SRCALPHA)
    pg.display.set_caption(TITLE)
    pg.display.set_icon(ICON)

    def end_game(title, score, message):
        EndScreen(surface, title, score, message).loop()

    def play_game():
        Game(surface, end_game).loop()

    MainMenu(surface, play_game).loop()
