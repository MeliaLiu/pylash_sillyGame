import random

from pylash.core import stage, addChild, KeyCode
from pylash.display import Sprite, BitmapData, Bitmap, TextField
from pylash.events import MouseEvent, LoopEvent, KeyboardEvent
from pylash.media import Sound
from pylash.ui import Button

gameBoard = []
candies = {}

gameContinue = True

for i in range(50):
    gameBoard.append([])
    for j in range(50):
        gameBoard[i].append(None)

class snake(Sprite):
    def __init__(self, snakeKind, startX, startY, direction):
        super(snake, self).__init__()
        self.snakeKind = snakeKind
        self.direction = direction
        self.startX = startX
        self.startY = startY
        self.speed = 1
        self.eatenCandies = 0
        self.score = 0
        self.heads = {
            "Up" : Bitmap(BitmapData(dataList[self.snakeKind+"HeadUp"])),
            "Down" : Bitmap(BitmapData(dataList[self.snakeKind+"HeadDown"])),
            "Left" : Bitmap(BitmapData(dataList[self.snakeKind+"HeadLeft"])),
            "Right" : Bitmap(BitmapData(dataList[self.snakeKind+"HeadRight"]))
        }
        for i in self.heads:
            playingLayer.addChild(self.heads[i])
            self.heads[i].visible = False
        self.items = [{"row":int(self.startY/10)-13, "col":int(self.startX/10)-1, "item":self.heads[self.direction]}]
        self.items[0]["item"].x = self.startX
        self.items[0]["item"].y = self.startY
        self.items[0]["item"].visible = True
        playingLayer.addChild(self.items[0]["item"])

        global gameBoard
        if (startX/10-1 >= 0) and (startY/10-13 >= 0):
            gameBoard[int(startY/10-13)][int(startX/10-1)] = "head"

        if self.direction == "Up":
            for i in range(5):
                self.addBody(self.startY+(1+i)*10, self.startX)
        elif  self.direction == "Down":
            for i in range(5):
                self.addBody(self.startY+(-1-i)*10, self.startX)
        elif self.direction == "Left":
            for i in range(5):
                self.addBody(self.startY, self.startX+(1+i)*10)
        elif self.direction == "Right":
            for i in range(5):
                self.addBody(self.startY, self.startX+(-1-i)*10)
        for i in gameBoard:
            for j in i:
                if j == "snake1":
                    boo = True
        print("snake init:", boo)

    def addBody(self, y, x):
        # global gameBoard
        item = Bitmap(BitmapData(dataList[self.snakeKind+"Body"]))
        item.x = x
        item.y = y
        playingLayer.addChild(item)
        self.items.append({"row":int(y/10)-13, "col":int(x/10)-1, "item":item}) # the row and col is wrt the gameBoard
        if (y/10-13 >= 0) and (x/10-1 >= 0):
            gameBoard[int(y/10-13)][int(x/10-1)] = self.snakeKind
    
    def move(self):
        # global gameBoard

        # head style
        lastHead = self.items[0]["item"]
        lastHead.visible = False
        self.items[0]["item"] = self.heads[self.direction]
        self.items[0]["item"].x = lastHead.x
        self.items[0]["item"].y = lastHead.y
        self.items[0]["item"].visible = True
        # create new bodies
        newBodies = []
        for i in range(self.eatenCandies):
            new = {"row":0, "col":0, "item":Bitmap(BitmapData(dataList[self.snakeKind+"Body"]))}
            new["item"].x = self.items[-self.speed+i]["item"].x
            new["item"].y = self.items[-self.speed+i]["item"].y
            new["row"] = self.items[-self.speed+i]["row"]
            new["col"] = self.items[-self.speed+i]["col"]
            newBodies.append(new)
            playingLayer.addChild(new["item"])
            gameBoard[new["row"]][new["col"]] = self.snakeKind
        self.eatenCandies = 0
        # move
        for i in range(len(self.items)-1, -1, -1):
            # clear gameBoard
            gameBoard[int(self.items[i]["row"])][int(self.items[i]["col"])] = None
            if (i - self.speed >= 0):
                # update images' position
                self.items[i]["item"].x = self.items[i-self.speed]["item"].x
                self.items[i]["item"].y = self.items[i-self.speed]["item"].y
                # update the dictionary's row and col
                self.items[i]["row"] = self.items[i-self.speed]["row"]
                self.items[i]["col"] = self.items[i-self.speed]["col"]
            else:
                if self.direction == "Up":
                    # update images' position
                    self.items[i]["item"].x = self.items[0]["item"].x
                    self.items[i]["item"].y = self.items[0]["item"].y - (self.speed-i) * 10
                    # update the dictionary's row and col
                    self.items[i]["col"] = self.items[0]["col"]
                    self.items[i]["row"] = self.items[0]["row"] - (self.speed-i)
                elif self.direction == "Down":
                    # update images' position
                    self.items[i]["item"].x = self.items[0]["item"].x
                    self.items[i]["item"].y = self.items[0]["item"].y + (self.speed-i) * 10
                    # update the dictionary's row and col
                    self.items[i]["col"] = self.items[0]["col"]
                    self.items[i]["row"] = self.items[0]["row"] + (self.speed-i)
                elif self.direction == "Left":
                    # update images' position
                    self.items[i]["item"].x = self.items[0]["item"].x - (self.speed-i) * 10
                    self.items[i]["item"].y = self.items[0]["item"].y
                    # update the dictionary's row and col
                    self.items[i]["col"] = self.items[0]["col"] - (self.speed-i)
                    self.items[i]["row"] = self.items[0]["row"]
                elif self.direction == "Right":
                    # update images' position
                    self.items[i]["item"].x = self.items[0]["item"].x + (self.speed-i) * 10
                    self.items[i]["item"].y = self.items[0]["item"].y
                    # update the dictionary's row and col
                    self.items[i]["col"] = self.items[0]["col"] + (self.speed-i)
                    self.items[i]["row"] = self.items[0]["row"]
            # Update the gameBoard
            if (i == 0):
                if (int(self.items[i]["row"]) < 0 or int(self.items[i]["row"]) > 49) or (int(self.items[i]["col"]) < 0 or int(self.items[i]["col"]) > 49):
                    print("speed:", self.speed)
                    print("direction:", self.direction)
                    print("overKind: \n", debugOverKind)
                    print("overInfo: \n", debugOverInfo)
                    print("row and col:", self.items[i]["row"], self.items[i]["col"])
                gameBoard[int(self.items[i]["row"])][int(self.items[i]["col"])] = "head"
                if self.direction == "Up":
                    nextHeadRow = self.items[0]["row"] - 1
                    nextHeadCol = self.items[0]["col"]
                elif self.direction == "Down":
                    nextHeadRow = self.items[0]["row"] + 1
                    nextHeadCol = self.items[0]["col"]
                elif self.direction == "Left":
                    nextHeadRow = self.items[0]["row"]
                    nextHeadCol = self.items[0]["col"] - 1
                elif  self.direction == "Right":
                    nextHeadRow = self.items[0]["row"]
                    nextHeadCol = self.items[0]["col"] + 1
            else:
                gameBoard[int(self.items[i]["row"])][int(self.items[i]["col"])] = self.snakeKind
            self.items[0]["item"].remove()
            playingLayer.addChild(self.items[0]["item"])
        
        # add newly grown bodies
        for newbody in newBodies:
            self.items.append(newbody)
        return (nextHeadRow, nextHeadCol)


def gameStart(data, bgmPlay, effectsPlay, p1Profile, p2Profile):
    global dataList, playingLayer, effectsOn, gameOverEffect, eatCandyEffects, moveEffect, btnEffect

    effectsOn = effectsPlay
    # receive the loaded data
    dataList = data

    gameOverEffect = Sound(dataList["gameOverEffect"])

    eatCandyEffects = [Sound(dataList["eatCandyEffect1"]),Sound(dataList["eatCandyEffect2"]),Sound(dataList["eatCandyEffect3"])]
    for eatCandyEffect in eatCandyEffects:
        eatCandyEffect.loopCount = 1

    moveEffect = Sound(dataList["moveEffect"])
    moveEffect.loopCount = Sound.LOOP_FOREVER

    btnEffect = Sound(dataList["btnEffect"])
    btnEffect.loopCount = 1

    # create the playing layer
    playingLayer = Sprite()
    addChild(playingLayer)

    # set the bg image
    playingBg = Bitmap(BitmapData(dataList["playingBg"], 0, 0, 520, 640))
    playingLayer.addChild(playingBg)

    # add profiles
    profile1 = Bitmap(BitmapData(dataList["profile%s" % p1Profile]))
    profile1.x = 20
    profile1.y = 20
    profile1.width = 100
    profile1.height = 100
    playingLayer.addChild(profile1)

    profile2 = Bitmap(BitmapData(dataList["profile%s" % p2Profile]))
    profile2.x = 400
    profile2.y = 20
    profile2.width = 100
    profile2.height = 100
    playingLayer.addChild(profile2) # display the scores
    colon = TextField()
    colon.text = ":"
    colon.size = 50
    colon.x = 260 - colon.width/2
    colon.y = 70 - colon.height/2
    colon.textColor = "#225590"
    colon.font = "Bradley Hand"
    playingLayer.addChild(colon)

    global snake1, snake2
    # create game snakes
    snake1 = snake("snake1", 60, 180, "Right")
    snake2 = snake("snake2", 450, 570, "Left")

    global score1Txt, score2Txt

    score1Txt = TextField()
    score1Txt.text = "%s" % snake1.score
    score1Txt.size = 50
    score1Txt.x = 260 - 20 - score1Txt.width
    score1Txt.y = 70 - score1Txt.height/2
    score1Txt.textColor = "#225590"
    score1Txt.font = "Bradley Hand"
    playingLayer.addChild(score1Txt)

    score2Txt = TextField()
    score2Txt.text = "%s" % snake2.score
    score2Txt.size = 50
    score2Txt.x = 260 + 20
    score2Txt.y = 70 - score2Txt.height/2
    score2Txt.textColor = "#225590"
    score2Txt.font = "Bradley Hand"
    playingLayer.addChild(score2Txt)

    # add sample snakes
    sampleSnake1 = snake("snake1", 130, 40, "Up")
    sampleSnake2 = snake("snake2", 380, 40, "Up")


    stage.addEventListener(KeyboardEvent.KEY_DOWN, keyDown)
    stage.addEventListener(KeyboardEvent.KEY_UP, keyUp)
    playingLayer.addEventListener(LoopEvent.ENTER_FRAME, loop)

    boo = False
    for i in gameBoard:
        for j in i:
            if j == "snake1":
                boo = True
    print("before generate:", boo)
    generate(0.05, 0)
    for i in gameBoard:
        for j in i:
            if j == "snake1":
                boo = True
    print("after generate:", boo)

def keyDown(e):
    # if e.keyCode == KeyCode.KEY_SPACE:
        # while (True):
        #     mode = input("index = 0 or output the gameBoard = 1\n")
        #     if mode == "0":
        #         row = input("row")
        #         col = input("col")
        #         print(gameBoard[row][col])
        #     else:
        #         for i in range(len(gameBoard)):
        #             print('------------- row:', i)
        #             print(gameBoard[i])
    if e.keyCode == KeyCode.KEY_W:
        snake1.direction = "Up"
        snake1.speed = 3
        moveEffect.play()
    elif e.keyCode == KeyCode.KEY_S:
        snake1.direction = "Down"
        snake1.speed = 3
        moveEffect.play()
    elif e.keyCode == KeyCode.KEY_A:
        snake1.direction = "Left"
        snake1.speed = 3
        moveEffect.play()
    elif e.keyCode == KeyCode.KEY_D:
        snake1.direction = "Right"
        snake1.speed = 3
        moveEffect.play()
    elif e.keyCode == KeyCode.KEY_I:
        snake2.direction = "Up"
        snake2.speed = 3
        moveEffect.play()
    elif e.keyCode == KeyCode.KEY_K:
        snake2.direction = "Down"
        snake2.speed = 3
        moveEffect.play()
    elif e.keyCode == KeyCode.KEY_J:
        snake2.direction = "Left"
        snake2.speed = 3
        moveEffect.play()
    elif e.keyCode == KeyCode.KEY_L:
        snake2.direction = "Right"
        snake2.speed = 3
        moveEffect.play()

def keyUp(e):
    if (e.keyCode == KeyCode.KEY_W) or (e.keyCode == KeyCode.KEY_S) or (e.keyCode == KeyCode.KEY_A) or (e.keyCode == KeyCode.KEY_D):
        snake1.speed = 1
        moveEffect.stop()
    elif (e.keyCode == KeyCode.KEY_I) or (e.keyCode == KeyCode.KEY_K) or (e.keyCode == KeyCode.KEY_J) or (e.keyCode == KeyCode.KEY_L):
        snake2.speed = 1
        moveEffect.stop()

def loop(e):
    minRatio = 0.045
    while (len(candies)/(2500-len(snake1.items)-len(snake2.items)) < minRatio):
        generate(0.05, 1)

    if gameContinue:
        snakeLoop(snake1, snake2)
    if gameContinue:
        snakeLoop(snake2, snake1)

def snakeLoop(s1, s2):
    normal = True     
    snakeCollision = False                                                      
    # record the position of s2
    s2Position = []
    # compute the next position of s2
    s2NextPosition = {}
    for i in range(len(s2.items)-1, -1, -1):
        s2Position.append((s2.items[i]["row"], s2.items[i]["col"]))

        if (i - s2.speed >= 0):
            # update the dictionary's row and col
            row = s2.items[i-s2.speed]["row"]
            col = s2.items[i-s2.speed]["col"]
        else:
            if s2.direction == "Up":
                # update the dictionary's row and col
                col = s2.items[0]["col"]
                row = s2.items[0]["row"] - (s2.speed-i)
            elif s2.direction == "Down":
                # update the dictionary's row and col
                col = s2.items[0]["col"]
                row = s2.items[0]["row"] + (s2.speed-i)
            elif s2.direction == "Left":
                # update the dictionary's row and col
                col = s2.items[0]["col"] - (s2.speed-i)
                row = s2.items[0]["row"]
            elif s2.direction == "Right":
                # update the dictionary's row and col
                col = s2.items[0]["col"] + (s2.speed-i)
                row = s2.items[0]["col"]
        col = int(col)
        row = int(row)
        if (i == 0):
            s2NextPosition[str(row)+"_"+str(col)] = "head"
        else:
            s2NextPosition[str(row)+"_"+str(col)] = "body"

    # check
    records = []
    for i in range(s1.speed):
        if s1.direction == "Up":
            row = s1.items[0]["row"]-1-i
            col = s1.items[0]["col"]
        elif s1.direction == "Down":
            row = s1.items[0]["row"]+1+i
            col = s1.items[0]["col"]
        elif s1.direction == "Left":
            row = s1.items[0]["row"]
            col = s1.items[0]["col"]-1-i
        elif s1.direction == "Right":
            row = s1.items[0]["row"]
            col = s1.items[0]["col"]+1+i

        row = int(row)
        col = int(col)
        if ((row < 0 or row > 49) or (col < 0 or col > 49)):
            normal = False
            gameOver("wall", {"snakeKind":s1.snakeKind})
        elif (str(row)+"_"+str(col) in s2NextPosition):
            normal = False
            snakeCollision = True
            if s2NextPosition[str(row)+"_"+str(col)] == "head":
                if (row, col) in s2Position:
                    records.append(["head", {"snakeKind":s1.snakeKind, "snakeToMove":[s1], "point":(row, col)}])
                else:
                    records.append(["head", {"snakeKind":s1.snakeKind, "snakeToMove":[s1, s2], "point":(row, col)}])
            elif s2NextPosition[str(row)+"_"+str(col)] == "body":
                if (row, col) in s2Position:
                    if (s1.direction == s2.direction):
                        records.append(["bodySameDirection", {"snakeKind":s1.snakeKind, "snakeToMove":[s1], "s2Position":s2Position}])
                    else:
                        records.append(["body", {"snakeKind":s1.snakeKind, "snakeToMove":[s1], "point":(row, col)}])
                else:
                    records.append(["body", {"snakeKind":s1.snakeKind, "snakeToMove":[s1, s2], "point":(row, col)}])
        elif (gameBoard[row][col] == "candy"):
            s1.eatenCandies += 1 
            s1.score += 1
            if s1 == snake1:
                score1Txt.text = s1.score
                score1Txt.x = 260 - 20 - score1Txt.width
                score1Txt.y = 70 - score1Txt.height/2
            else:
                score2Txt.text = s1.score
                score2Txt.x = 260 + 20
                score2Txt.y = 70 - score2Txt.height/2

            candies[str(row)+"_"+str(col)].remove()
            gameBoard[row][col] = None
            del candies[str(row)+"_"+str(col)]

    if effectsOn and (s1.eatenCandies != 0):
        eatCandyEffects[s1.eatenCandies-1].play()

    if normal:
        s1.move()
    elif snakeCollision:
        gameOver(records[-1][0], records[-1][-1])
    
def generate(ratio, candyKind):
    global candies, gameBoard

    boo = False 
    for i in gameBoard:
        for j in i:
            if j == "snake1":
                boo = True
    print("directly before really generate:", boo)

    while (len(candies)/(2500-len(snake1.items)-len(snake2.items)) < ratio):
        row = random.randint(0, 49)
        col = random.randint(0, 49)

        if (gameBoard[row][col] == None):
            gameBoard[row][col] = "candy"
            # candyKind = random.randint(0,3)
            newCandy = Bitmap(BitmapData(dataList["candy%s" % candyKind]))
            newCandy.x = 10 + col*10
            newCandy.y = 130 + row*10
            playingLayer.addChild(newCandy)
            candies[str(row)+"_"+str(col)] = newCandy



def gameOver(overKind, overInfo):
    global debugOverKind, debugOverInfo
    debugOverKind = overKind
    debugOverInfo = overInfo

    if effectsOn:
        gameOverEffect.play()
    global gameContinue
    gameContinue = False
    playingLayer.removeAllEventListeners()
    if overInfo["snakeKind"] == "snake1":
        snake = snake1
    else:
        snake = snake2


    # adjust the positions
    winner = ["P1"]
    snake1.speed = 1
    snake2.speed = 1
    snake1.eatenCandies = 0
    snake2.eatenCandies = 0
    if (overKind == "wall"):
        if overInfo["snakeKind"] == "snake1":
            winner[0] = "P2"
        while True:

            if (snake.items[0]["row"] <= 0 or snake.items[0]["row"] >= 49) or (snake.items[0]["col"] <= 0 or snake.items[0]["col"] >= 49):
                break
            else:
                snake.move()
    elif overKind == "head":
        if snake1.score == snake2.score:
            winner = []
        elif snake1.score < snake2.score:
            winner[0] = "P2"

        for s in overInfo["snakeToMove"]:
            while (s.items[0]["row"], s.items[0]["col"]) != overInfo["point"]:
                s.move()
    elif (overKind == "body"):
        if overInfo["snakeKind"] == "snake1":
            winner[0] = "P2"

        for s in overInfo["snakeToMove"]:
            while (s.items[0]["row"], s.items[0]["col"]) != overInfo["point"]:
                s.move()
    elif (overKind == "bodySameDirection"):
        if overInfo["snakeKind"] == "snake1":
            winner[0] = "P2"

        for s in overInfo["snakeToMove"]:
            while not((s.items[0]["row"], s.items[0]["col"]) in overInfo["s2Position"]):
                s.move()

    lastHead = snake.items[0]["item"]
    lastHead.visible = False
    newHead = Bitmap(BitmapData(dataList[snake.snakeKind+"Head"+snake.direction]))
    newHead.x = lastHead.x
    newHead.y = lastHead.y
    playingLayer.addChild(newHead)

    # display the faces
    p1Face = TextField()
    playingLayer.addChild(p1Face)
    if "P1" in winner:
        p1Face.text = "😂"
    else:
        p1Face.text = "😭"
    p1Face.size = 50
    p1Face.x = 20 + 50 - p1Face.width/2
    p1Face.y = 20 + 50 - p1Face.height/2

    p2Face = TextField()
    playingLayer.addChild(p2Face)
    if "P2" in winner:
        p2Face.text = "😂"
    else:
        p2Face.text = "😭"
    p2Face.size = 50
    p2Face.x = 400 + 50 - p2Face.width/2
    p2Face.y = 20 + 50 - p2Face.height/2


    # define the state of buttons
    normal = Bitmap(BitmapData(dataList["normalLeaveBtn"]))
    over = Bitmap(BitmapData(dataList["actionLeaveBtn"]))
    down = Bitmap(BitmapData(dataList["actionLeaveBtn"]))
    normal.alpha = 0.5
    over.alpha = 0.75
    down.alpha = 0.75

    leaveBtn = Button(normal, over, down, None)
    leaveBtn.x = 135
    leaveBtn.y = 130+250-leaveBtn.height/2
    playingLayer.addChild(leaveBtn)

    def next(e):
        btnEffect.play()
        exit()
        
    leaveBtn.addEventListener(MouseEvent.MOUSE_UP, next)
    leaveBtn.addEventListener(MouseEvent.MOUSE_DOWN, btnEffectPlay)

def btnEffectPlay(e):
    if effectsOn:
        btnEffect.play()
        

    