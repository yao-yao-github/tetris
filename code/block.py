import pygame
from pygame import K_LEFT, K_RIGHT, K_UP, K_DOWN

from code.const import BLOCK_RES, GAME_COL, BLOCK_SHAPE, GAME_WIDTH_SIZE, GAME_HEIGHT_SIZE
from code.utils import getCurrentTime



class Block(pygame.sprite.Sprite):
    def __init__(self, blockType, baseRowIdx, baseColIdx, blockShape, blockRot, blockGroupIdx, width, height, relPos):
        super().__init__()
        self.blockType = blockType
        self.baseRowIdx = baseRowIdx
        self.baseColIdx = baseColIdx
        self.blockShape = blockShape
        self.blockRot = blockRot
        self.blockGroupIdx = blockGroupIdx
        self.width = width
        self.height = height
        self.relPos = relPos
        self.blink = False
        self.blinkCount = 0
        self.loadImage()
        self.updateImagePos()

    # 启动消除前闪烁
    def startBlink(self):
        self.blink = True
        self.blinkTime = getCurrentTime()

    def setBaseIndex(self, baseRowIdx, baseColIdx):
        self.baseRowIdx = baseRowIdx
        self.baseColIdx = baseColIdx

    def loadImage(self):
        self.image = pygame.image.load(BLOCK_RES[self.blockType])
        self.image = pygame.transform.scale(self.image, (self.width, self.height))

    # 更新图片位置
    def updateImagePos(self):
        self.rect = self.image.get_rect()
        left = self.relPos[0] + self.width * self.colIdx
        if left > GAME_WIDTH_SIZE:
            left = GAME_WIDTH_SIZE
        self.rect.left = left
        top = self.relPos[1] + self.height * self.rowIdx
        if top > GAME_HEIGHT_SIZE:
            top = GAME_HEIGHT_SIZE
        self.rect.top = top


    def draw(self, surface):
        self.updateImagePos()
        # 闪烁的关键：原理是除不尽时，不渲染到页面上
        if self.blink and self.blinkCount % 2 == 0:
            return
        # 绘制移动后的图像到屏幕上
        surface.blit(self.image, self.rect)

    # 下降逻辑：为方块增加行数
    def drop(self):
        self.baseRowIdx += 1

    # 获取行和列的索引
    def getIndex(self):
        return (int(self.rowIdx), int(self.colIdx))

    # 获取下一个块的行和列的索引
    def getNextIndex(self):
        return (int(self.rowIdx + 1), int(self.colIdx))

    # 获取左侧块索引位置
    def getLeftIndex(self):
        return (int(self.rowIdx ), int(self.colIdx - 1))

    # 获取右侧块索引位置
    def getRightIndex(self):
        return (int(self.rowIdx ), int(self.colIdx + 1))

    def isLeftBound(self):
        return self.baseColIdx == 0

    def isRightBound(self):
        return self.colIdx == GAME_COL - 1

    def doLeft(self):
        self.baseColIdx -= 1

    def doRight(self):
        self.baseColIdx += 1

    # 获取方块组合
    def getBlockConfigIndex(self):
        return BLOCK_SHAPE[self.blockShape][self.blockRot][self.blockGroupIdx]

    @property
    def rowIdx(self):
        return self.baseRowIdx + self.getBlockConfigIndex()[0]

    @property
    def colIdx(self):
        return self.baseColIdx + self.getBlockConfigIndex()[1]

    def doLeft(self):
        self.baseColIdx -= 1

    def doRight(self):
        self.baseColIdx += 1

    def drop(self):
        self.baseRowIdx += 1

    # 设置方块旋转角度
    def doRotate(self):
        self.blockRot += 1
        if self.blockRot >= len(BLOCK_SHAPE[self.blockShape]):
            self.blockRot = 0

    def update(self):
        if self.blink:
            diffTime = getCurrentTime() - self.blinkTime
            self.blinkCount = int(diffTime / 30)



