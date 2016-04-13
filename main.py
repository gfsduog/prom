from serial import Serial
from time import time

BLACK = 0
NET = RED = 1
GREEN = 2
SCORE = WHITE = 3
BLUE = 4
MAGENTA = 5
BAT = CYAN = 6 # bats
BALL = YELLOW = 7

COLOURS = ('\033[40m', '\033[41m', '\033[42m', '\033[47m', '\033[44m', '\033[45m', '\033[46m', '\033[43m')

WIDTH = 80
HEIGHT = 20

Player0Score = 0
Player1Score = 0
Player0OldBat = 9
Player1OldBat = 9
Player0Bat = 9
Player1Bat = 9

def bugger():
    bugger = WIDTH * HEIGHT * [BLACK]

    bugger[WIDTH / 2 + WIDTH * 2] = NET
    bugger[WIDTH / 2 + WIDTH * 3] = NET
    bugger[WIDTH / 2 + WIDTH * 6] = NET
    bugger[WIDTH / 2 + WIDTH * 7] = NET
    bugger[WIDTH / 2 + WIDTH * 10] = NET
    bugger[WIDTH / 2 + WIDTH * 11] = NET
    bugger[WIDTH / 2 + WIDTH * 14] = NET
    bugger[WIDTH / 2 + WIDTH * 15] = NET
    bugger[WIDTH / 2 + WIDTH * 18] = NET
    bugger[WIDTH / 2 + WIDTH * 19] = NET
    
    for i in range(3):
        bugger[2 + WIDTH * (Player0Bat + i)] = BAT
    for i in range(3):
        bugger[77 + WIDTH * (Player1Bat + i)] = BAT
    return bugger

def delta():
    delta = [[] for i in range(len(COLOURS))]
    for i in range(WIDTH * HEIGHT):
        if oldBugger[i] != currentBugger[i]:
            delta[currentBugger[i]].append(i)
    return delta

def output(delta):
    for i, colour in enumerate(delta):
        if colour:
            write(COLOURS[i])
            prev = colour[0]
            write('\033[' + str(prev / WIDTH + 1) + ';' + str(prev % WIDTH + 1) + 'H ')
            for i in range(1, len(colour)):
                i = colour[i]
                if prev + 1 != i:
                    write('\033[' + str(i / WIDTH + 1) + ';' + str(i % WIDTH + 1) + 'H')
                write(' ')

with Serial('/dev/ttyAMA0') as cereal:
    write = cereal.write
    write('\033[?25l')
    oldBugger = WIDTH * HEIGHT * [None]
    oldTime = time()
    while True:
        newTime = time()
        print 1/(newTime - oldTime)
        currentBugger = bugger()
        output(delta())
        oldBugger = currentBugger
        cereal.flush()
        oldTime = newTime
