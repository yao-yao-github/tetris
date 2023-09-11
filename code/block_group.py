import random
from pygame.locals import *


from code.const import *
from code.block import *
from code.utils import *


# 检查降落块左右移动时是否触碰到固定块
def checkCollision(fixedBlockGroup, checkObject):
    hash = {}
    allIndexes = fixedBlockGroup.getBlockIndexes()
    for idx in allIndexes:
        hash[idx] = 1
    for idx in checkObject:
        if hash.get(idx):
            return False
    return True


class BlockGroup(object):

    # @staticmethod
    # def GenerateBlockGroupConfig(rowIdx, colIdx):
    #     idx = random.randint(0, len(BLOCK_SHAPE) - 1)
    #     bType = random.randint(0, BlockType.BLOCKMAX - 1)
    #     configList = []
    #     for x in range(len(BLOCK_SHAPE[idx])):
    #         config = {
    #             'blockType': bType,
    #             'rowIdx': rowIdx + BLOCK_SHAPE[idx][x][0],
    #             'colIdx': colIdx + BLOCK_SHAPE[idx][x][1]
    #         }
    #         configList.append(config)
    #     return configList

    # 增加了方块旋转的逻辑代码
    @staticmethod
    def GenerateBlockGroupConfig(rowIdx, colIdx):
        shapeIdx = random.randint(0, len(BLOCK_SHAPE) - 1)
        bType = random.randint(0, BlockType.BLOCKMAX - 1)
        configList = []
        rotIdx = 0
        for i in range(len(BLOCK_SHAPE[shapeIdx][rotIdx])):
            config = {
                'blockType': bType,
                'blockShape': shapeIdx,
                'blockRot': rotIdx,
                'blockGroupIdx': i,
                'rowIdx': rowIdx,
                'colIdx': colIdx
            }
            configList.append(config)
        return configList

    def __init__(self, blockGroupType, width, height, blockConfigList, relPos, dropInterval=800):
        super(BlockGroup, self).__init__()
        self.blocks = []
        self.time = getCurrentTime()
        self.pressTime = {}
        self.blockGroupType = blockGroupType
        self.isEliminating = False
        self.dropInterval = dropInterval
        self.eliminateRowDict = {}
        self.eliminateTime = 0
        for config in blockConfigList:
            blk = Block(config['blockType'], config['rowIdx'], config['colIdx'], config['blockShape'],
                        config['blockRot'], config['blockGroupIdx'], width, height, relPos)
            self.blocks.append(blk)

    def setBaseIndexes(self, baseRow, baseCol):
        for blk in self.blocks:
            blk.setBaseIndex(baseRow, baseCol)

    def draw(self, surface):
        for blk in self.blocks:
            blk.draw(surface)

    def update(self, fixedBlockGroup=None):
        oldTime = self.time
        curTime = getCurrentTime()
        diffTime = curTime - oldTime
        if self.blockGroupType == BlockGroupType.DROP:
            if diffTime >= self.dropInterval:
                self.time = curTime
                for b in self.blocks:
                    b.drop()
            self.keyDownHandler(fixedBlockGroup)
        # 首次固定块fixedBlockGroup运行时，因为blocks中没有对象，所以不会进行循环，此处是为了触发消除闪烁效果
        for blk in self.blocks:
            blk.update()

        if self.IsEliminating():
            # 消除方块并带有闪烁效果
            if getCurrentTime() - self.eliminateTime > 500:
                tmpBlocks = []
                for blk in self.blocks:
                    if not self.eliminateRowDict.get(blk.getIndex()[0]):
                        for row in self.eliminateRowDict.keys():
                            if blk.getIndex()[0] <= row:
                                blk.drop()
                        tmpBlocks.append(blk)
                self.blocks = tmpBlocks
                self.setEliminate(False)

    def getBlockIndexes(self):
        return [block.getIndex() for block in self.blocks]

    def getNextBlockIndexes(self):
        return [block.getNextIndex() for block in self.blocks]

    def getLeftBlockIndexes(self):
        return [block.getLeftIndex() for block in self.blocks]

    def getRightBlockIndexes(self):
        return [block.getRightIndex() for block in self.blocks]

    def getBlocks(self):
        return self.blocks

    def clearBlocks(self):
        self.blocks = []

    def addBlocks(self, blk):
        self.blocks.append(blk)

    # 检查按键是否过快
    def checkAndSetPressTime(self, key):
        ret = False
        if getCurrentTime() - self.pressTime.get(key, 0) > 30:
            ret = True
        self.pressTime[key] = getCurrentTime()
        return ret

    def checkCanClickDown(self):
        flag = False
        if getCurrentTime() - self.time > 100:
            flag = True
        return flag

    # 按键控制函数
    def keyDownHandler(self, fixedBlockGroup):
        pressed = pygame.key.get_pressed()
        b = True
        if pressed[K_LEFT] and self.checkAndSetPressTime(K_LEFT):
            for blk in self.blocks:
                if blk.isLeftBound():
                    b = False
                    break
            if b and checkCollision(fixedBlockGroup, self.getLeftBlockIndexes()):
                for blk in self.blocks:
                    blk.doLeft()
        elif pressed[K_RIGHT] and self.checkAndSetPressTime(K_RIGHT):
            bl = self.getMaxColBlock()
            if bl.isRightBound():
                b = False
            if b and checkCollision(fixedBlockGroup, self.getRightBlockIndexes()):
                for blk in self.blocks:
                    blk.doRight()

        if pressed[K_DOWN] and self.checkCanClickDown():
            self.dropInterval = 20

        if pressed[K_UP] and self.checkAndSetPressTime(K_UP) and checkCollision(fixedBlockGroup, self.getLeftBlockIndexes()) and checkCollision(fixedBlockGroup, self.getRightBlockIndexes()):
            if self.checkLongBlockGroup():
                if not self.checkLongBlockGroupCanRotate(fixedBlockGroup):
                    return
            if self.checkLBlockGroup():
                if not self.checkLBlockGroupCanRotate(fixedBlockGroup):
                    return
            for blk in self.blocks:
                blk.doRotate()
            self.checkAndSetBlocksPosition()

    # 检查是否为长条块组
    def checkLongBlockGroup(self):
        longShape = True
        longBlock = BLOCK_SHAPE[1][1]
        shapeList = [(bl.getBlockConfigIndex()) for bl in self.blocks]
        for long in range(len(longBlock)):
            if longBlock[long][0] != shapeList[long][0] and longBlock[1] != shapeList[long][1]:
                longShape = False
                break
        return longShape

    # 检查长条块组可否旋转
    def checkLongBlockGroupCanRotate(self, fixedBlockGroup):
        flag = True
        hash = {}
        allIndexes = fixedBlockGroup.getBlockIndexes()
        for blk in allIndexes:
            hash[blk] = 1
        for bl in self.blocks:
            if hash.get((bl.getIndex()[0], bl.getIndex()[1] + 2)) or\
                    hash.get((bl.getIndex()[0], bl.getIndex()[1] + 3)) or\
                    hash.get((bl.getIndex()[0], bl.getIndex()[1] - 2)) or\
                    hash.get((bl.getIndex()[0], bl.getIndex()[1] - 3)):
                flag = False
                break
        return flag

    # 检查是否为L块组
    def checkLBlockGroup(self):
        lShape = True
        lBlock = BLOCK_SHAPE[4][3]
        shapeList = [(bl.getBlockConfigIndex()) for bl in self.blocks]
        for long in range(len(lBlock)):
            if lBlock[long][0] != shapeList[long][0] and lBlock[1] != shapeList[long][1]:
                lShape = False
                break
        return lShape

    # 检查L块组可否旋转
    def checkLBlockGroupCanRotate(self, fixedBlockGroup):
        flag = True
        hash = {}
        allIndexes = fixedBlockGroup.getBlockIndexes()
        for blk in allIndexes:
            hash[blk] = 1
        bl = self.blocks[3]
        if hash.get((bl.getIndex()[0], bl.getIndex()[1] + 2)):
            flag = False
        return flag

    # 检查并修改块位置
    def checkAndSetBlocksPosition(self):
        blm = self.getMaxColBlock()
        exceed_value = blm.colIdx - GAME_COL + 1
        if exceed_value > 0:
            for blk in self.blocks:
                blk.baseColIdx -= exceed_value

    # 取得组中的最大列的块
    def getMaxColBlock(self):
        max_block = self.blocks[0]
        for block in self.blocks:
            if block.colIdx > max_block.colIdx:
                max_block = block
        return max_block

    # 方块消除函数
    def doEliminate(self, rowDict):
        eliminateRow = {}
        for row in rowDict.keys():
            for col in range(0, GAME_COL):
                idx = (row, col)
                eliminateRow[idx] = 1
        self.setEliminate(True)
        # 把要消除的行赋值
        self.eliminateRowDict = rowDict
        for blk in self.blocks:
            # 再次确认，如果被消除行存在于固定块组中，则启动闪烁
            if eliminateRow.get(blk.getIndex()):
                blk.startBlink()

    # 方块消除逻辑
    def processEliminate(self):
        hash = {}
        score = 0
        allIndexes = self.getBlockIndexes()
        for idx in allIndexes:
            hash[idx] = 1
        eliminateRowDict = {}
        # 这里倒序的话会有问题
        for row in range(0, GAME_ROW + 1):
            full = True
            for col in range(0, GAME_COL):
                index = (row, col)
                # 如果未找到行中任意一列的方块，则终止循环，且判定为未满足消除条件
                if not hash.get(index):
                    full = False
                    break
            if full:
                eliminateRowDict[row] = 1
                score += 1
        if len(eliminateRowDict) > 0:
            self.doEliminate(eliminateRowDict)
        return score

    def setEliminate(self, el):
        self.isEliminating = el
        self.eliminateTime = getCurrentTime()

    def IsEliminating(self):
        return self.isEliminating
