import copy
import random
import numpy as np
colorNum = 5
tileNum = 5
levelNum = 500
levelType = 1

mry = 0

def exchangeTile(level,position,tile):
    level[position].append(tile)
    newtile = level[position][0]
    del level[position][0]
    return newtile,level

for i in range(levelNum):
    colorNum = random.randint(5, 7)
    tileNum = random.randint(5, 7)
    levelType = random.randint(0, 2)
    hand = 0
    level =[[0 for _ in range(tileNum)] for _ in range(colorNum)]
    for i in range(0,colorNum,1):
        for j in range(0,tileNum,1):
            level[i][j] = i+1
    random.shuffle(level)
    # print(level)
    move = random.randint(10, colorNum*tileNum)
    if levelType == 0:
        for i in range(0,move,1):
            movedata = exchangeTile(level,random.randint(0,colorNum-1),hand)
            hand = movedata[0]
            level =movedata[1]

        print(hand,"|",move+15,"|",level)
    if levelType == 1:
        for i in range(0,move,1):
            movedata = exchangeTile(level,random.randint(0,colorNum-1),hand)
            hand = movedata[0]
            level =movedata[1]

        questionMark = [[0 for _ in range(3)] for _ in range(random.randint(colorNum-2,colorNum+2))]
        for data in questionMark:
            data[1]=random.randint(0,colorNum-1)
            data[2] = random.randint(0, tileNum -2 )
        # print(questionMark)
        # print(np.unique(questionMark, axis=0).tolist())
        # print("--------------------")
        if len(np.unique(questionMark, axis=0).tolist()) <2:
            mry = mry+1
            # print(mry/levelNum)
        while len(np.unique(questionMark, axis=0).tolist())< colorNum-2:
            # print("触发条件，开始处理")

            data1 = random.randint(0, colorNum-1)
            data2 = random.randint(0, tileNum-2)
            questionMark.append([0,data1,data2])
            questionMark = np.unique(questionMark, axis=0).tolist()

        print(hand,"|",move+20,"|",level,"|",questionMark)
    if levelType == 2:
        for i in range(0,move,1):
            movedata = exchangeTile(level,random.randint(0,colorNum-1),hand)
            hand = movedata[0]
            level =movedata[1]

        ice = random.randint(0, colorNum-1)
        levelcopy = copy.copy(level)
        del levelcopy[ice]
        # print(levelcopy)
        # print(level)
        noIce = []
        noIce.append(hand)

        for data in levelcopy:
            for num in data:
                noIce.append(num)

        # print(noIce)
        colorNumTure = 0
        for i in range(0,colorNum,1):
            # print(i,noIce.count(i))
            # print(tileNum)
            if noIce.count(i) == tileNum:
                colorNumTure=colorNumTure+1
        # print(colorNumTure)
        if colorNumTure!=0:
            iceNum = random.randint(1, colorNumTure)
            icedata = []
            icedata.append([1,ice,iceNum])
            print(hand, "|", move + iceNum*5, "|", level, "|", icedata)

