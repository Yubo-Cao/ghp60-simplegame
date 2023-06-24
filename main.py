import pygame as pg

from game import Game, MainMenu

pg.init()


def play_game():
    with Game() as game:
        while True:
            game.loop()

            for evt in pg.event.get():
                if evt.type == pg.QUIT:
                    return


if __name__ == "__main__":
    menu = MainMenu(Game.SIZE[0], Game.SIZE[1], play_game)
    menu.main_menu()
    pg.quit()