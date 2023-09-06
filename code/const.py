class BlockType:
    RED = 0
    ORANGE = 1
    YELLOW = 2
    GREEN = 3
    CYAN = 4
    BLUE = 5
    PURPLE = 6
    BLOCKMAX = 7


class BlockGroupType:
    FIXED = 0
    DROP = 1


BLOCK_RES = {
    BlockType.RED: "./pic/tetris/red.png",
    BlockType.ORANGE: "./pic/tetris/orange.png",
    BlockType.YELLOW: "./pic/tetris/yellow.png",
    BlockType.GREEN: "./pic/tetris/green.png",
    BlockType.CYAN: "./pic/tetris/cyan.png",
    BlockType.BLUE: "./pic/tetris/blue.png",
    BlockType.PURPLE: "./pic/tetris/purple.png"
}

GAME_ROW = 17
GAME_COL = 10

BLOCK_SIZE_W = 40
BLOCK_SIZE_H = 40

GAME_WIDTH_SIZE = 1000
GAME_HEIGHT_SIZE = 800


# BLOCK_SHAPE = [
#     [(0, 0), (0, 1), (1, 0), (1, 1)],  # 方形
#     [(0, 0), (0, 1), (0, 2), (0, 3)],  # 长条
#     [(0, 0), (1, 0), (1, 1), (1, 2)],  # z字
#     [(0, 1), (1, 0), (1, 1), (1, 2)]   # 土型
# ]

BLOCK_SHAPE = [
    [((0, 0), (0, 1), (1, 0), (1, 1))],                                     # 方形
    [((0, 0), (0, 1), (0, 2), (0, 3)), ((0, 0), (1, 0), (2, 0), (3, 0))],   # 长条
    [((0, 0), (0, 1), (1, 1), (1, 2)), ((0, 1), (1, 0), (1, 1), (2, 0))],   # z字
    [((0, 1), (1, 0), (1, 1), (1, 2)), ((0, 0), (1, 0), (1, 1), (2, 0)), ((1, 0), (1, 1), (1, 2), (2, 1)), ((0, 1), (1, 0), (1, 1), (2, 1))],    # 土型
    [((0, 0), (1, 0), (1, 1), (1, 2)), ((0, 1), (1, 1), (2, 0), (2, 1)), ((0, 0), (0, 1), (0, 2), (1, 2)), ((0, 0), (0, 1), (1, 0), (2, 0))],  # L形

]










