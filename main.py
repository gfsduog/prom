from serial import Serial
from smbus import SMBus
import RPi.GPIO as gpio
from time import time
from random import uniform

BLACK = 0
NET = RED = 1
GREEN = 2
SCORE = WHITE = 3
BLUE = 4
MAGENTA = 5
BAT = CYAN = 6
BALL = YELLOW = 7

LEDS = (5, 6, 12, 13, 16, 19, 20, 26)

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

BASE_SPEED = 8. / WIDTH

Player0Score = 0
Player1Score = 0
Player0Bat = 0
Player1Bat = 0
Player0Height = 3
Player1Height = 3
ServeCount = 0
Serving = True
BallXSpeed = 1
BallYSpeed = 1
Player0SizeCounter = 15
Player0Megabats = 2
Player1SizeCounter = 15
Player1Megabats = 2


def bugger():
    bugger = WIDTH * HEIGHT * [BLACK]

    for i in range(2, HEIGHT - 1, 4):
        bugger[WIDTH / 2 + i * WIDTH] = NET
        bugger[WIDTH / 2 + (i + 1) * WIDTH] = NET
    
    for i in SCORES[Player0Score]:
        bugger[WIDTH / 2 - 10 + i] = SCORE
    for i in SCORES[Player1Score]:
        bugger[WIDTH / 2 + 8 + i] = SCORE

    for i in range(Player0Height):
        bugger[2 + (Player0Bat + i) * WIDTH] = BAT
    for i in range(Player1Height):
        bugger[WIDTH - 3 + (Player1Bat + i) * WIDTH] = BAT

    bugger[BallX + BallY * WIDTH] = BALL

    return bugger

def output():
    delta = [[] for i in COLOURS]
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

def megabat(port):
    global Player0Megabats, Player0Height, Player1Megabats, Player1Height, Player0SizeCounter, Player1SizeCounter
    if port == 9 and Player0Megabats:
        Player0Height <<= 1
        Player0Megabats -= 1
        Player0SizeCounter = 0
    elif port == 4 and Player1Megabats:
        Player1Height <<= 1
        Player1Megabats -= 1
        Player1SizeCounter = 0

with Serial('/dev/ttyAMA0', 115200) as cereal:
    adc = SMBus(1)
    write = cereal.write
    write('\033[?25l')
    gpio.setwarnings(False)
    gpio.setmode(gpio.BCM)
    gpio.setup(4, gpio.IN, gpio.PUD_UP)
    gpio.setup(9, gpio.IN, gpio.PUD_UP)
    gpio.add_event_detect(4, gpio.FALLING, megabat, 15000)
    gpio.add_event_detect(9, gpio.FALLING, megabat, 15000)
    gpio.setup(10, gpio.IN, gpio.PUD_UP)
    gpio.setup(11, gpio.IN, gpio.PUD_UP)
    for led in LEDS: gpio.setup(led, gpio.OUT)
    oldBugger = WIDTH * HEIGHT * [None]
    oldTime = time()
    counter = 0
    while 1:
        newTime = time()
        counter += newTime - oldTime
        adc.write_byte(33, 128)
        knob = adc.read_word_data(33, 0)
        Player0Bat = HEIGHT - int(round(((knob & 15) << 8 | knob >> 8) * (HEIGHT - Player0Height) / 4096.)) - Player0Height
        adc.write_byte(33, 16)
        knob = adc.read_word_data(33, 0)
        Player1Bat = HEIGHT - int(round(((knob & 15) << 8 | knob >> 8) * (HEIGHT - Player1Height) / 4096.)) - Player1Height
        if Player0SizeCounter < 15: Player0SizeCounter += newTime - oldTime
        else: Player0Height = 3
        if Player1SizeCounter < 15: Player1SizeCounter += newTime - oldTime
        else: Player1Height = 3
        if Serving:
            if ServeCount < 5:
                BallY = Player0Bat + Player0Height / 2
                BallX = 3
            else:
                BallY = Player1Bat + Player1Height / 2
                BallX = WIDTH - 4
            Serving = gpio.input(10) and ServeCount < 5 or gpio.input(11) and ServeCount >= 5
            if not Serving:
                threshold = BASE_SPEED * uniform(.5, 1.5)
                counter = 0
        else:
            while counter >= threshold:
                counter -= threshold
                BallX += BallXSpeed
                BallY += BallYSpeed
                if BallX == 0 or BallX == WIDTH - 1:
                    Serving = True
                    ServeCount = (ServeCount + 1) % 10
                    if BallX == 0: Player1Score += 1
                    else: Player0Score += 1
                    BallXSpeed = 1 if ServeCount < 5 else -1
                if BallX == 2 and 0 <= BallY - Player0Bat < Player0Height or BallX == WIDTH - 3 and 0 <= BallY - Player1Bat < Player1Height:
                    BallXSpeed = -BallXSpeed
                    BallX += BallXSpeed
                    if BallX == 3:
                        BallYSpeed = 3 * (BallY - Player0Bat) / Player0Height - 1
                    else:
                        BallYSpeed = 3 * (BallY - Player1Bat) / Player1Height - 1
                    threshold = BASE_SPEED * uniform(.5, 1.5)
                if BallY == -1 or BallY == HEIGHT:
                    BallYSpeed = -BallYSpeed
                    BallY += BallYSpeed
        for led in LEDS: gpio.output(led, False)
        gpio.output(LEDS[8 * BallX / (WIDTH + 1)], True)
        print(Player0Megabats, Player1Megabats)
        currentBugger = bugger()
        output()
        oldBugger = currentBugger
        cereal.flush()
        oldTime = newTime
