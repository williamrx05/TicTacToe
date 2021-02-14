class position:
    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y

    def getx(self) -> int:
        return self.x

    def gety(self) -> int:
        return self.y

    def text(self) -> str:
        return "(" + str(self.x) + ", " + str(self.y) + ")"

class tictactoe:
    def __init__(self, b: [[int]] = None):
        if not b:
            self.board = [[0 for _ in range(3)] for _ in range(3)]
            for x in range(3):
                for y in range(3):
                    self.board[x][y] = 0
        else:
            self.board = [[0 for _ in range(3)] for _ in range(3)]
            for x in range(3):
                for y in range(3):
                    self.board[x][y] = b[x][y]

    def __deepcopy__(self, memodict={}):
        copy = type(self)()
        memodict[id(self)] = copy
        for x in range(3):
            for y in range(3):
                copy.addpiece(x, y, self.board[x][y])
        return copy

    def addpiece(self, x: int, y: int, side: int):
        self.board[x][y] = side

    def openpieces(self):
        openspots = []
        for x in range(3):
            for y in range(3):
                if self.board[x][y] == 0:
                    openspots.append(position(x, y))
        return openspots

    def state(self) -> int:
        # diagonals
        if self.board[0][0] == self.board[1][1] == self.board[2][2] or self.board[2][0] == self.board[1][1] == self.board[0][2]:
            return self.board[1][1]
        elif self.board[0][0] == self.board[0][1] == self.board[0][2]:
            return self.board[0][0]
        elif self.board[1][0] == self.board[1][1] == self.board[1][2]:
            return self.board[1][0]
        elif self.board[2][0] == self.board[2][1] == self.board[2][2]:
            return self.board[2][0]
        elif self.board[0][0] == self.board[1][0] == self.board[2][0]:
            return self.board[0][0]
        elif self.board[0][1] == self.board[1][1] == self.board[2][1]:
            return self.board[0][1]
        elif self.board[0][2] == self.board[1][2] == self.board[2][2]:
            return self.board[0][2]
        return 0

    def printboard(self) -> int:
        print("")
        for y in range(2, -1, -1):
            for x in range(3):
                if self.board[x][y] == 0:
                    print(" ` ", end='')
                elif self.board[x][y] == -1:
                    print(" O ", end='')
                elif self.board[x][y] == 1:
                    print(" X ", end='')
            print("")

board = tictactoe()
depth_max = 4
depth_min = 4
def result(s: tictactoe, p: position, side: int):
    memo = {}
    t = s.__deepcopy__(memo)
    t.addpiece(p.getx(), p.gety(), side)
    return t

def max_value(s: tictactoe, d: int = depth_max, a: int=-9999, b: int=9999):
    v = -9999
    pos = None
    d -= 1
    memo = {}
    t = s.__deepcopy__(memo)
    value = t.state()
    if value != 0 or len(t.openpieces()) == 0:
        return value
    for position in t.openpieces():
        prev = v
        m = min_value(result(t, position, 1), d, a, b)
        v = max(v, m)
        a = max(a, v)
        if not prev == v or not pos:
            pos = position
        if b <= a:
            break
    if d == depth_max - 1:
        s.addpiece(pos.getx(), pos.gety(), 1)
    return v


def min_value(s: tictactoe, d: int=depth_min, a: int=-9999, b: int=9999):
    v = 9999
    pos = None
    d -= 1
    memo = {}
    t = s.__deepcopy__(memo)
    value = t.state()
    if value != 0 or len(t.openpieces()) == 0:
        return value
    for position in t.openpieces():
        prev = v
        m = max_value(result(t, position, -1), d, a, b)
        v = min(v, m)
        b = min(b, v)
        if not prev == v or not pos:
            pos = position
        if b <= a:
            break
    if d == depth_max - 1:
        s.addpiece(pos.getx(), pos.gety(), -1)
    return v

while(True):
    min_value(board)
    board.printboard()
    if board.state() != 0 or len(board.openpieces()) == 0:
        break
    max_value(board)
    board.printboard()
    if board.state() != 0 or len(board.openpieces()) == 0:
        break