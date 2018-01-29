import missionConfig

# Game mover
boats = []
rafts = []
# tigers = []
# bears = []

# Game object
coins = []
bridges = []
islands = []

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
        return self._x

    @property
    def y(self):
        return self._y


'''
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
'''


class coinObj(gameObj):
    def setStatus(self, status):
        self.status = status

    def gold(self):
        if self.status[-4:] == 'gold':
            return True
        else:
            return False

    def silver(self):
        if self.status[:6] == 'silver':
            return True
        else:
            return False

class mover(gameObj):
    def move(self, distance):
        if isinstance(distance, (int,float)):
            pass
        else:
            raise TypeError("move() take a number argument.")

    def turn(self, direction):
        if isinstance(direction, (str)):
            pass
        else:
            raise TypeError("turn() take a number argument.")

    def goto(self,obj):
        if isinstance(obj, gameObj):
            pass
        else:
            raise TypeError("goto() take a game object argument.")

    def turnLeft(self, obj):
        if isinstance(obj, gameObj):
            pass
        else:
            raise TypeError("turnLeft() take a game object argument.")

    def turnRight(self, obj):
        if isinstance(obj, gameObj):
            pass
        else:
            raise TypeError("turnRight() take a game object argument.")


class heroObj(mover):
    def __init__(self, name):
        self.name = name

    def attack(self, obj):
        pass


class petObj(mover):
    def __init__(self, name):
        self.name = name

    def attack(self):
        pass


class boatObj(mover):
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
    'coins': [coins, coinObj, 'coins[{0}]'],
    'boats': [boats, boatObj, 'boats[{0}]'],
    'bridges': [bridges, gameObj, 'bridges[{0}]'],
    'islands': [islands, gameObj, 'islands[{0}]'],
    'rafts': [rafts, gameObj, 'rafts[{0}]']
}
hero = heroObj('hero')
pet = petObj('pet')
coin = coinObj('coin')
boat = boatObj('boat')
bridge = gameObj('bridge')
island = gameObj('island')
raft = gameObj('raft')