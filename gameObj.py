import missionConfig
# Game animal
goats = []
turtles = []
crocodiles = []
beavers = []
tigers = []
bears = []
# Game object
bananas = []
bridges = []
islands = []
rafts = []
bushes = []

def init(missionNum):
    missionInfo = missionConfig.missionInfo[str(missionNum)]
    for obj in missionInfo:
        objName = obj[0]
        objArray = objDict[objName][0]
        if len(objArray)>0:
            del objArray[:]
        objSingle = objDict[objName][1]
        objString = objDict[objName][2]
        if objName == 'bananas':
            for i,status in enumerate(obj[-1]):
                bObj = objSingle(objString.format(i))
                bObj.setStatus(status)
                objArray.append(bObj)
        else:
            for i in range(obj[-1]):
                objArray.append(objSingle(objString.format(i)))
def distanceTo(obj):
    if isinstance(obj, gameObj):
        return 15
    else:
        raise TypeError("distanceTo() take a game object argument.")


def commandEnd():
    pass

class gameObj(object):
    def __init__(self, name):
        self.name = name
        self._x = 0
        self._y = 0

    def setPos(self,pos):
        self._x = pos['x']
        self._y = pos['y']

    def distanceTo(self, obj):
        if isinstance(obj, gameObj):
            return 15
        else:
            raise TypeError("distanceTo() take a game object argument.")

    @property
    def x(self):
        return self._xhy

    @property
    def y(self):
        return self._y

class bananaObj(gameObj):
    def setStatus(self, status):
        self.status = status

    def green(self):
        if self.status[-5:] == 'green':
            return True
        else:
            return False

    def frozen(self):
        if self.status[:6] == 'frozen':
            return True
        else:
            return False

    def rotten(self):
        if self.status[-5:] == 'rotten':
            return True
        else:
            return False

class mover(gameObj):
    def step(self,distance):
        if isinstance(distance, (int,float)):
            pass
        else:
            raise TypeError("step() take a number argument.")

    def turn(self,angle):
        if isinstance(angle, (int,float)):
            pass
        else:
            raise TypeError("turn() take a number argument.")

    def goto(self,obj):
        if isinstance(obj, gameObj):
            pass
        else:
            raise TypeError("goto() take a game object argument.")

    def turnTo(self,obj):
        if isinstance(obj, gameObj):
            pass
        else:
            raise TypeError("turnTo() take a game object argument.")

class monkeyObj(mover):
    def toss(self,obj):
        pass

class goatObj(mover):
    def __init__(self, name):
        self.name = name
    def hit(self):
        pass

class turtleObj(mover):
    def setPos(self, pos):
        self.pos.x = pos.x
        self.pos.y = pos.y

class crocodileObj(mover):
    def setPos(self, pos):
        self.pos.x = pos.x
        self.pos.y = pos.y

class predatorObj(gameObj):
    def __init__(self, name):
        self.name = name
        self._x = 0
        self._y = 0
        self._sleeping = False
        self._playing = False

    def play(self):
        self._playing = True

    def sleep(self):
        self._sleeping = True

    @property
    def playing(self):
        return self._playing

    @property
    def sleeping(self):
        return self._sleeping

objDict = {
    'bananas':[bananas, bananaObj, 'bananas[{0}]'],
    'goats': [goats, goatObj, 'goats[{0}]'],
    'turtles': [turtles, turtleObj, 'turtles[{0}]'],
    'crocodiles': [crocodiles, crocodileObj, 'crocodiles[{0}]'],
    'beavers': [beavers, mover, 'beavers[{0}]'],
    'tigers': [tigers, predatorObj, 'tigers[{0}]'],
    'bears': [bears, predatorObj, 'bears[{0}]'],
    'bridges': [bridges, gameObj, 'bridges[{0}]'],
    'islands': [islands, gameObj, 'islands[{0}]'],
    'rafts': [rafts, gameObj, 'rafts[{0}]'],
    'bushes': [bushes, gameObj, 'bushes[{0}]']
}
monkey = monkeyObj('monkey')
goat = goatObj('goat')
banana = bananaObj('banana')
turtle = turtleObj('turtle')
crocodile = crocodileObj('crocodile')
beaver = mover('beaver')
tiger = predatorObj('tiger')
bear = predatorObj('bear')
bridge = gameObj('bridge')
island = gameObj('island')
raft = gameObj('raft')
bush = gameObj('bush')