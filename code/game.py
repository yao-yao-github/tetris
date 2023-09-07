import pygame
from pygame import K_SPACE

from code.block_group import BlockGroup
from code.const import *


class Game(pygame.sprite.Sprite):
    def __init__(self, surface):
        self.surface = surface
        self.fixedBlockGroup = BlockGroup(BlockGroupType.FIXED, BLOCK_SIZE_W, BLOCK_SIZE_H, [], self.getRelPos())
        self.dropBlockGroup = None
        self.gameOverImage = pygame.image.load('./pic/tetris/lose.png')
        self.scoreFont = pygame.font.Font(None, 60)
        self.score = 0
        self.isGameOver = False
        self.nextBlockGroup = None
        self.generateNextBlockGroup()

    # 旧的生成新的方块代码
    # def generateDropBlockGroup(self):
    #     conf = BlockGroup.GenerateBlockGroupConfig(0,s GAME_COL / 2 - 1)
    #     self.dropBlockGroup = BlockGroup(BlockGroupType.DROP, BLOCK_SIZE_W, BLOCK_SIZE_H, conf, self.getRelPos())

    def generateDropBlockGroup(self):
        self.dropBlockGroup = self.nextBlockGroup
        self.dropBlockGroup.setBaseIndexes(0, GAME_COL / 2 - 1)
        self.generateNextBlockGroup()

    def generateNextBlockGroup(self):
        conf = BlockGroup.GenerateBlockGroupConfig(0, GAME_COL + 3)
        self.nextBlockGroup = BlockGroup(BlockGroupType.DROP, BLOCK_SIZE_W, BLOCK_SIZE_H, conf, self.getRelPos())

    def draw(self):
        self.fixedBlockGroup.draw(self.surface)
        if self.dropBlockGroup:
            self.dropBlockGroup.draw(self.surface)
        self.nextBlockGroup.draw(self.surface)
        if self.isGameOver:
            rect = self.gameOverImage.get_rect()
            rect.centerx = GAME_WIDTH_SIZE / 2
            rect.centery = GAME_HEIGHT_SIZE / 2
            # 把游戏结束图片绘制图像到屏幕上
            self.surface.blit(self.gameOverImage, rect)
            self.restart()

        scoreTextImage = self.scoreFont.render('Score: ' + str(self.score), True, (255, 255, 255))
        # 把积分绘制图像到屏幕上
        self.surface.blit(scoreTextImage, (10, 10))

    # 设置所渲染出的坐标
    def getRelPos(self):
        return (250, 50)

    def willCollide(self):
        hash = {}
        allIndexes = self.fixedBlockGroup.getBlockIndexes()
        for idx in allIndexes:
            hash[idx] = 1

        dropIndexes = self.dropBlockGroup.getNextBlockIndexes()

        for dropIndex in dropIndexes:
            if hash.get(dropIndex):
                return True
            if dropIndex[0] >= GAME_ROW:
                return True
        return False

    def update(self):
        if self.isGameOver:
            return
        # 检查是否游戏结束
        self.checkGameOver()

        self.fixedBlockGroup.update()

        # 检测是否为正在消除
        if self.fixedBlockGroup.IsEliminating():
            return

        # 判断是否有下落块组，如果没有则生成下落块组
        if self.dropBlockGroup:
            self.dropBlockGroup.update(self.fixedBlockGroup)
        else:
            self.generateDropBlockGroup()

        if self.willCollide():
            blocks = self.dropBlockGroup.getBlocks()
            for blk in blocks:
                self.fixedBlockGroup.addBlocks(blk)
            self.dropBlockGroup.clearBlocks()
            self.dropBlockGroup = None
            self.score += self.fixedBlockGroup.processEliminate()

    def checkGameOver(self):
        allIndexes = self.fixedBlockGroup.getBlockIndexes()
        for idx in allIndexes:
            # 判断小于两行时设置结束游戏为True
            if idx[0] < 2:
                self.isGameOver = True

    def restart(self):
        pressed = pygame.key.get_pressed()
        if pressed[K_SPACE]:
            self.fixedBlockGroup.clearBlocks()
            self.isGameOver = False
