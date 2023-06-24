import os
import sys

import pygame

from .burger import BurgerClass
from .player import Player

pygame.init()
pygame.font.init()

score = 0
score_increment = 1


def collision():
    if Player.colliderect(BurgerClass):
        score += score_increment


font = pygame.font.Front(None, 36)
score_text = font.render(f"Score: {score}", True, (255, 255, 255))
