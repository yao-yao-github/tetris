import sys

import pygame

from pygame.locals import QUIT

from code.const import *
from code.game import Game


pygame.init()

DISPLAYSURF = pygame.display.set_mode((GAME_WIDTH_SIZE, GAME_HEIGHT_SIZE))

pygame.display.set_caption("Yao Game")

game = Game(DISPLAYSURF)

while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
    game.update()
    # 清空屏幕
    DISPLAYSURF.fill((135, 206, 235))
    game.draw()

    pygame.display.update()







