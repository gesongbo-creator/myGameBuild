import random
import numpy as np
import sys

needLevelNum = 100
dotsNum = 4
mapsize = 5
obstacleNum =2
obstacleType = -1



# 做一个找数字0的函数
def findZero(map):
    zero_positions = [(i, j) for i, row in enumerate(map) for j, val in enumerate(row) if val == 0]
    if not zero_positions:
        return None  # 没有找到 0
    return random.choice(zero_positions)


def mapPrint(map):
    for row in map:
        print(row)

def findAir(map,positions):
    # print(positions)
    air = []
    x = positions[0]
    y = positions[1]
    # print(x)
    x1 = x-1
    x2 = x+1
    y1 = y-1
    y2 = y+1
    if x1>=0 and map[x1][y] == 0:
        findAirPositition = (x1,y)
        air.append(findAirPositition)
    if x2<len(map) and map[x2][y] == 0:
        findAirPositition = (x2,y)
        air.append(findAirPositition)
    if y1>=0 and map[x][y1] == 0:
        findAirPositition = (x,y1)
        air.append(findAirPositition)
    if y2<len(map) and map[x][y2] == 0:
        findAirPositition = (x,y2)
        air.append(findAirPositition)
    return air


while needLevelNum > 0:
    # 初始化关卡的地图
    map = [[0 for _ in range(mapsize)] for _ in range(mapsize)]

    # 根据障碍物数量去生成障碍的
    if obstacleNum != 0:
        for i in range(0, obstacleNum, 1):
            map[random.randint(0, mapsize - 1)][random.randint(0, mapsize - 1)] = obstacleType

    # 找到线的初始位置
    dotsLocation = []
    for dotsLocationNum in range(0, dotsNum, 1):
        dotsLocation.append([])
    for i in range(0, dotsNum, 1):
        if findZero(map) == None:
            print("初始化的地图没有空位")
            sys.exit(0)
        else:
            location = findZero(map)
            dotsLocation[i].append(location)
            map[location[0]][location[1]] = i + 1

    # 找到初始位置后依次移动
    while 1:
        wrong = 0
        # print("计数器")
        # print(dotsLocation)
        for i in range (0, dotsNum, 1):
            # print(dotsLocation[i])
            air = findAir(map, dotsLocation[i][-1])
            # print(air)
            if air != []:
                num =random.randint(0, len(air)-1)
                map[air[num][0]][air[num][1]] = i+1
                dotsLocation[i].append(air[num])
            else:
                wrong += 1
        if wrong == dotsNum:
            break

    # mapPrint(map)
    # needLevelNum -= 1
    # mapPrint(dotsLocation)
    mypass = 0
    for i in range(0, dotsNum, 1):
        if len(dotsLocation[i]) < 3:
            mypass = 1
    if findZero(map) == None and mypass == 0:
        needLevelNum -= 1
        print(dotsLocation)
        # mapPrint(map)