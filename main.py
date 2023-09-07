import sys

import pygame

from pygame.locals import QUIT

from code.const import *
from code.game import Game

pygame.init()

DISPLAYSURF = pygame.display.set_mode((GAME_WIDTH_SIZE, GAME_HEIGHT_SIZE))

pygame.display.set_caption("Yao Game")

game = Game(DISPLAYSURF)

line_color = (255, 255, 255)  # 线的颜色，这里使用白色
line_width = 5  # 线的宽度


while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
    game.update()
    # 背景绘制为天蓝色
    DISPLAYSURF.fill((135, 206, 235))
    game.draw()
    # 绘制边界线
    pygame.draw.line(DISPLAYSURF, line_color, (250, 20), (250, 733), line_width)  # 左边界线
    pygame.draw.line(DISPLAYSURF, line_color, (653, 20), (653, 733), line_width)  # 右边界线
    pygame.draw.line(DISPLAYSURF, line_color, (250, 732), (653, 732), line_width)  # 下边界线

    pygame.display.update()
