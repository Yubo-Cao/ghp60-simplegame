import pygame as pg

from game import Game

if __name__ == "__main__":
    with Game() as game:
        while True:
            game.loop()

            for evt in pg.event.get():
                if evt.type == pg.QUIT:
                    pg.quit()
                    exit()
