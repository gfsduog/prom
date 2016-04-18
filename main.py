from serial import Serial
from smbus import SMBus
from time import time

BLACK = 0
NET = RED = 1
GREEN = 2
SCORE = WHITE = 3
BLUE = 4
MAGENTA = 5
BAT = CYAN = 6
BALL = YELLOW = 7

COLOURS = ('\033[40m', '\033[41m', '\033[42m', '\033[47m', '\033[44m', '\033[45m', '\033[46m', '\033[43m')

WIDTH = 80
HEIGHT = 40

SCORES = (
(WIDTH, WIDTH + 1, WIDTH + 2, WIDTH * 2, WIDTH * 2 + 2, WIDTH * 3, WIDTH * 3 + 2, WIDTH * 4, WIDTH * 4 + 2, WIDTH * 5, WIDTH * 5 + 1, WIDTH * 5 + 2),
(WIDTH + 2, WIDTH * 2 + 2, WIDTH * 3 + 2, WIDTH * 4 + 2, WIDTH * 5 + 2),
(WIDTH, WIDTH + 1, WIDTH + 2, WIDTH * 2 + 2, WIDTH * 3, WIDTH * 3 + 1, WIDTH * 3 + 2, WIDTH * 4, WIDTH * 5, WIDTH * 5 + 1, WIDTH * 5 + 2),
(WIDTH, WIDTH + 1, WIDTH + 2, WIDTH * 2 + 2, WIDTH * 3, WIDTH * 3 + 1, WIDTH * 3 + 2, WIDTH * 4 + 2, WIDTH * 5, WIDTH * 5 + 1, WIDTH * 5 + 2),
(WIDTH, WIDTH + 2, WIDTH * 2, WIDTH * 2 + 2, WIDTH * 3, WIDTH * 3 + 1, WIDTH * 3 + 2, WIDTH * 4 + 2, WIDTH * 5 + 2),
(WIDTH, WIDTH + 1, WIDTH + 2, WIDTH * 2, WIDTH * 3, WIDTH * 3 + 1, WIDTH * 3 + 2, WIDTH * 4 + 2, WIDTH * 5, WIDTH * 5 + 1, WIDTH * 5 + 2),
(WIDTH, WIDTH + 1, WIDTH + 2, WIDTH * 2, WIDTH * 3, WIDTH * 3 + 1, WIDTH * 3 + 2, WIDTH * 4, WIDTH * 4 + 2, WIDTH * 5, WIDTH * 5 + 1, WIDTH * 5 + 2),
(WIDTH, WIDTH + 1, WIDTH + 2, WIDTH * 2 + 2, WIDTH * 3 + 2, WIDTH * 4 + 2, WIDTH * 5 + 2),
(WIDTH, WIDTH + 1, WIDTH + 2, WIDTH * 2, WIDTH * 2 + 2, WIDTH * 3, WIDTH * 3 + 1, WIDTH * 3 + 2, WIDTH * 4, WIDTH * 4 + 2, WIDTH * 5, WIDTH * 5 + 1, WIDTH * 5 + 2),
(WIDTH, WIDTH + 1, WIDTH + 2, WIDTH * 2, WIDTH * 2 + 2, WIDTH * 3, WIDTH * 3 + 1, WIDTH * 3 + 2, WIDTH * 4 + 2, WIDTH * 5 + 2),
)

Player0Score = 0
Player1Score = 0
Player0Bat = 0
Player1Bat = 0
BallX = WIDTH/2
BallY = HEIGHT/2
BallXSpeed = 1
BallYSpeed = 1

def bugger():
    bugger = WIDTH * HEIGHT * [BLACK]

    for i in range(2, HEIGHT, 4):
        bugger[WIDTH / 2 + WIDTH * i] = NET
        bugger[WIDTH / 2 + WIDTH * (i + 1)] = NET
    
    for i in SCORES[Player0Score]:
        bugger[WIDTH / 2 - 10 + i] = SCORE
    for i in SCORES[Player1Score]:
        bugger[WIDTH / 2 + 8 + i] = SCORE

    for i in range(3):
        bugger[2 + WIDTH * (Player0Bat + i)] = BAT
    for i in range(3):
        bugger[WIDTH - 3 + WIDTH * (Player1Bat + i)] = BAT

    return bugger

def output():
    delta = [[] for i in range(len(COLOURS))]
    for i in range(WIDTH * HEIGHT):
        if oldBugger[i] != currentBugger[i]:
            delta[currentBugger[i]].append(i)
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

with Serial('/dev/ttyAMA0', 115200) as cereal:
    adc = SMBus(1)
    write = cereal.write
    write('\033[?25l')
    oldBugger = WIDTH * HEIGHT * [None]
    oldTime = time()
    while True:
        newTime = time()
        print 1 / (newTime - oldTime)
        adc.write_byte(33, 128)
        knob = adc.read_word_data(33, 0)
        Player0Bat = int(round(((((knob & 15) << 8) | (knob >> 8)) / 4096.) * (HEIGHT - 3)))
        adc.write_byte(33, 0x40)
        knob = adc.read_word_data(33, 0)
        Player1Bat = int(round(((((knob & 15) << 8) | (knob >> 8)) / 4096.) * (HEIGHT - 3)))
        currentBugger = bugger()
        output()
        oldBugger = currentBugger
        cereal.flush()
        oldTime = newTime
