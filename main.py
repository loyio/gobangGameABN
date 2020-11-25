"""
 @Project: gobangGameABN
 @Author: Loyio
 @Date: 2020/11/14
"""

import random
import pygame
import datetime
from AlgoFunc.main import *

pygame.init()

space = 50  # 左边距
cell_size = 35.7  # 每个格子大小
cell_num = 15

pygame.display.set_caption('五子棋人机对战')
screen = pygame.display.set_mode((600, 600))

DEPTH = 3
ATK_RATIO = 1  # 攻击系数

listCPU = []
listSelf = []
listAll = []
listBlit = []

tableListAll = []

flag = 1

for i in range(cell_num + 1):
    for j in range(cell_num + 1):
        tableListAll.append((i, j))

perfectNext = [0, 0]
game_state = 1


def cpuAI(inFirst):
    """
    电脑运算主程序
    :param inFirst:是否是先手
    :return:最佳候选坐标
    """
    if inFirst:
        perfectNext[0] = random.randint(6, 8)
        perfectNext[1] = random.randint(6, 8)
    else:
        global cut_count
        global seek_count
        cut_count = 0
        seek_count = 0
        begin_time = datetime.datetime.now()
        abnAlgo(DEPTH, -99999999, 99999999, True)
        end_time = datetime.datetime.now()
        print("本次搜索次数: " + str(seek_count) + " 本次剪枝次数:" + str(cut_count) + " 总耗时: " + str(end_time - begin_time))
    return perfectNext[0], perfectNext[1]


def abnAlgo(depth, alpha_value, beta_value, is_computer):
    """
    负极大值搜索，alpha-beta 剪枝 主算法
    :param depth: 遍历深度
    :param alpha_value:alpha的值，初始时为负无穷大
    :param beta_value:beta的值，初始时为无穷大
    :param is_computer:是否是电脑方
    :return:alpha_value
    """
    if checkWin(listCPU) or checkWin(listSelf) or depth == 0:
        return evaluation(is_computer)

    blank_list = list(set(tableListAll).difference(set(listAll)))
    order(listAll, blank_list)
    for step in blank_list:
        global seek_count
        seek_count += 1

        # 忽略没有相邻棋子的点
        if not has_neighbor(step, listAll):
            continue

        if is_computer:
            listCPU.append(step)
        else:
            listSelf.append(step)
        listAll.append(step)

        value = -abnAlgo(depth - 1, -beta_value, -alpha_value, not is_computer)
        if is_computer:
            listCPU.remove(step)
        else:
            listSelf.remove(step)
        listAll.remove(step)

        if value > alpha_value:
            if depth == DEPTH:
                perfectNext[0] = step[0]
                perfectNext[1] = step[1]
            # 剪枝点
            if value >= beta_value:
                global cut_count
                cut_count += 1
                return beta_value
            alpha_value = value

    return alpha_value


def evaluation(is_computer):
    """
    评估函数
    :param is_computer: 是否是电脑方
    :return:总评分
    """
    total_score = 0

    if is_computer:
        self_list = listCPU
        rival_list = listSelf
    else:
        self_list = listSelf
        rival_list = listCPU

    # 算自己的得分
    score_all_arr = []
    my_score = 0
    for pt in self_list:
        m = pt[0]
        n = pt[1]
        my_score += calcScore(m, n, 0, 1, rival_list, self_list, score_all_arr)
        my_score += calcScore(m, n, 1, 0, rival_list, self_list, score_all_arr)
        my_score += calcScore(m, n, 1, 1, rival_list, self_list, score_all_arr)
        my_score += calcScore(m, n, -1, 1, rival_list, self_list, score_all_arr)

    #  算敌人的得分， 并减去
    score_all_arr_enemy = []
    enemy_score = 0
    for pt in rival_list:
        m = pt[0]
        n = pt[1]
        enemy_score += calcScore(m, n, 0, 1, self_list, rival_list, score_all_arr_enemy)
        enemy_score += calcScore(m, n, 1, 0, self_list, rival_list, score_all_arr_enemy)
        enemy_score += calcScore(m, n, 1, 1, self_list, rival_list, score_all_arr_enemy)
        enemy_score += calcScore(m, n, -1, 1, self_list, rival_list, score_all_arr_enemy)

    total_score = my_score - enemy_score * ATK_RATIO

    return total_score


first = input("请输入电脑是否先手(1/0):")
flag = int(first) + 1

change = int(first)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        piece = 1
        if change % 2 == 1 and game_state == 1:
            print("CPU running!!!")
            if first:
                aipos = cpuAI(first)
                first = 0
            else:
                aipos = cpuAI(first)
            if (aipos[0], aipos[1], 1) not in listBlit and (aipos[0], aipos[1], 2) not in listBlit:
                print("最优坐标: %d %c" % (aipos[1] + 1, aipos[0] + 65))
                listBlit.append((aipos[0], aipos[1], flag))
                listCPU.append(aipos)
                listAll.append(aipos)
                if checkWin(listCPU):
                    game_state = 2 if flag == 1 else 3
                else:
                    flag = 2 if flag == 1 else 1
                change += 1
        else:
            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = pygame.mouse.get_pos()  # 获取鼠标位置
                xi = int(round((x - space) * 1.0 / cell_size))  # 获取到x方向上取整的序号
                yi = int(round((y - space) * 1.0 / cell_size))  # 获取到y方向上取整的序号
                if 0 <= xi < cell_num and 0 <= yi < cell_num and (xi, yi, 1) not in listBlit and (
                        xi, yi, 2) not in listBlit:
                    listSelf.append((xi, yi))
                    listAll.append((xi, yi))
                    listBlit.append((xi, yi, flag))
                    if checkWin(listSelf):
                        game_state = 2 if flag == 1 else 3
                    else:
                        flag = 2 if flag == 1 else 1
                    change += 1

    chessBoardBG = pygame.image.load("resource/chessboard.png")
    screen.blit(chessBoardBG, (0, 0))

    for x, y, f in listBlit:
        chess_color = (30, 30, 30) if f == 1 else (225, 225, 225)
        pygame.draw.circle(screen, chess_color, [x * cell_size + space, y * cell_size + space], 16, 16)

    pygame.draw.rect(screen, (255, 0, 0), [perfectNext[0] * cell_size + space - cell_size / 2,
                                           perfectNext[1] * cell_size + space - cell_size / 2, cell_size, cell_size], 1)

    if game_state != 1:
        if game_state == 2:
            blackWin = pygame.image.load("resource/blackWin.bmp")
            screen.blit(blackWin, (166, 239))
        elif game_state == 3:
            whiteWin = pygame.image.load("resource/whiteWin.bmp")
            screen.blit(whiteWin, (166, 239))
        else:
            draw = pygame.image.load("resource/draw.bmp")
            screen.blit(draw, (166, 239))

    pygame.display.update()  # 必须调用update才能看到绘图显示
