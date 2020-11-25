"""
 @Project: gobangGameABN
 @Author: Loyio
 @Date: 2020/11/14
"""

# 分数形状
shape_score = [(50, (0, 1, 1, 0, 0)),
               (50, (0, 0, 1, 1, 0)),
               (200, (1, 1, 0, 1, 0)),
               (500, (0, 0, 1, 1, 1)),
               (500, (1, 1, 1, 0, 0)),
               (5000, (0, 1, 1, 1, 0)),
               (5000, (0, 1, 0, 1, 1, 0)),
               (5000, (0, 1, 1, 0, 1, 0)),
               (5000, (1, 1, 1, 0, 1)),
               (5000, (1, 1, 0, 1, 1)),
               (5000, (1, 0, 1, 1, 1)),
               (5000, (1, 1, 1, 1, 0)),
               (5000, (0, 1, 1, 1, 1)),
               (50000, (0, 1, 1, 1, 1, 0)),
               (99999999, (1, 1, 1, 1, 1))]


def checkFull(cell_num, chess_list):
    """
    检查棋盘是否填满
    :param cell_num:棋盘宽度
    :param chess_list:总填子列表
    :return:Ture or False
    """
    if len(chess_list) >= cell_num*cell_num:
        return True
    else:
        return False


def checkWin(chess_list):
    """
    检查是否有5子连线
    :param chess_list:落子列表
    :return:True or False
    """
    ROW = 15
    COLUMN = 15
    for m in range(COLUMN):
        for n in range(ROW):

            if n < ROW - 4 and (m, n) in chess_list and (m, n + 1) in chess_list and (m, n + 2) in chess_list and (
                    m, n + 3) in chess_list and (m, n + 4) in chess_list:
                return True
            elif m < ROW - 4 and (m, n) in chess_list and (m + 1, n) in chess_list and (m + 2, n) in chess_list and (
                        m + 3, n) in chess_list and (m + 4, n) in chess_list:
                return True
            elif m < ROW - 4 and n < ROW - 4 and (m, n) in chess_list and (m + 1, n + 1) in chess_list and (
                        m + 2, n + 2) in chess_list and (m + 3, n + 3) in chess_list and (m + 4, n + 4) in chess_list:
                return True
            elif m < ROW - 4 and n > 3 and (m, n) in chess_list and (m + 1, n - 1) in chess_list and (
                        m + 2, n - 2) in chess_list and (m + 3, n - 3) in chess_list and (m + 4, n - 4) in chess_list:
                return True
    return False


def calcScore(m, n, directionX, directionY, rivalList, selfList, allScoreList):
    """
    计算各方向的分值
    :param m:落子点X
    :param n:落子点Y
    :param directionX:X方向
    :param directionY:Y方向
    :param rivalList:对手方下棋点列表
    :param selfList:自己的下棋点列表
    :param allScoreList:所有的得分
    :return:分值
    """
    add_score = 0
    max_score_shape = (0, None)

    for item in allScoreList:
        for pt in item[1]:
            if m == pt[0] and n == pt[1] and directionX == item[2][0] and directionY == item[2][1]:
                return 0

    for offset in range(-5, 1):
        # offset = -2
        pos = []
        for i in range(0, 6):
            if (m + (i + offset) * directionX, n + (i + offset) * directionY) in rivalList:
                pos.append(2)
            elif (m + (i + offset) * directionX, n + (i + offset) * directionY) in selfList:
                pos.append(1)
            else:
                pos.append(0)
        tmp_shap5 = (pos[0], pos[1], pos[2], pos[3], pos[4])
        tmp_shap6 = (pos[0], pos[1], pos[2], pos[3], pos[4], pos[5])

        for (score, shape) in shape_score:
            if tmp_shap5 == shape or tmp_shap6 == shape:

                if score > max_score_shape[0]:
                    max_score_shape = (score, ((m + (0 + offset) * directionX, n + (0 + offset) * directionY),
                                               (m + (1 + offset) * directionX, n + (1 + offset) * directionY),
                                               (m + (2 + offset) * directionX, n + (2 + offset) * directionY),
                                               (m + (3 + offset) * directionX, n + (3 + offset) * directionY),
                                               (m + (4 + offset) * directionX, n + (4 + offset) * directionY)),
                                       (directionX, directionY))

    if max_score_shape[1] is not None:
        for item in allScoreList:
            for pt1 in item[1]:
                for pt2 in max_score_shape[1]:
                    if pt1 == pt2 and max_score_shape[0] > 10 and item[0] > 10:
                        add_score += item[0] + max_score_shape[0]

        allScoreList.append(max_score_shape)

    return add_score + max_score_shape[0]


def order(list_all, blank_list):
    """
    进行优先排序
    :param list_all: 所有落子点列表
    :param blank_list: 为填子点列表
    :return:none
    """
    last_pt = list_all[-1]
    for item in blank_list:
        for i in range(-1, 2):
            for j in range(-1, 2):
                if i == 0 and j == 0:
                    continue
                if (last_pt[0] + i, last_pt[1] + j) in blank_list:
                    blank_list.remove((last_pt[0] + i, last_pt[1] + j))
                    blank_list.insert(0, (last_pt[0] + i, last_pt[1] + j))


def has_neighbor(piece, list_all):
    """
    判断落子点是否有相邻的点
    :param piece: 落子点
    :param list_all: 所有已落子点
    :return:true or false
    """
    for i in range(-1, 2):
        for j in range(-1, 2):
            if i == 0 and j == 0:
                continue
            if (piece[0] + i, piece[1] + j) in list_all:
                return True
    return False
