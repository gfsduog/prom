from serial import Serial
from smbus import SMBus
import RPi.GPIO as gpio
from time import time, sleep
from random import uniform
from PyGlow import PyGlow

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

N_GS = 103.8
N_A = 110.
N_B = 123.5
N_C = 130.8
N_D = 146.8
N_E = 164.8
N_F = 174.6
N_G = 196.
N_GSH = 207.7
N_AH = 220.
N_R = 1.

N_BOUNCE = 500.0
N_SCORE = 1000.0

SONG_1_BPM = 144.
c = 1/(SONG_1_BPM/60)
SONG =   ((N_E,c),    # 1
          (N_B,c/2),
          (N_C,c/2),
          (N_D,c),
          (N_C,c/2),
          (N_B,c/2),
          (N_A,c),    # 2
          (N_A,c/2),
          (N_C,c/2),
          (N_E,c),
          (N_D,c/2),
          (N_C,c/2),
          (N_B,c*1.5),# 3
          (N_C,c/2),
          (N_D,c),
          (N_E,c),
          (N_C,c),    # 4
          (N_A,c),
          (N_A,c/2),
          (N_A,c/2),
          (N_B,c/2),
          (N_C,c/2),
          (N_D,c*1.5), # 5
          (N_F,c/2),
          (N_AH,c),
          (N_G,c/2),
          (N_F,c/2),
          (N_E,c*1.5), # 6
          (N_C,c/2),
          (N_E,c),
          (N_D,c/2),
          (N_C,c/2),
          (N_B,c),    #7
          (N_B,c/2),
          (N_C,c/2),
          (N_D,c),
          (N_E,c),
          (N_C,c),    # 8
          (N_A,c),
          (N_A,c),
          (N_R,c),
          (N_E,c*2), # 9
          (N_C,c*2),
          (N_D,c*2), # 10
          (N_B,c*2),
          (N_C,c*2), # 11
          (N_A,c*2),
          (N_GS,c*2), # 12
          (N_B,c),
          (N_R,c),
          (N_E,c*2), # 13
          (N_C,c*2),
          (N_D,c*2), # 14
          (N_B,c*2),
          (N_C,c), # 15
          (N_E,c),
          (N_AH,c*2),
          (N_GSH,c*2), # 17
          (N_R,c*2))

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

glow = PyGlow()

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
    gpio.setup(17, gpio.OUT)
    gpio.setup(18, gpio.OUT)
    # start music
    p = gpio.PWM(18,1)
    p.start(50)
    sfxStartTime = time()
    sfxLength = .2
    # music
    for note in SONG:
        p.ChangeFrequency(note[0])
        sleep(note[1])
    p.stop()
    p.ChangeFrequency(N_BOUNCE)
    for led in LEDS: gpio.setup(led, gpio.OUT)
    oldBugger = WIDTH * HEIGHT * [None]
    oldTime = time()
    counter = 0
    sorry = True
    while 1:
        newTime = time()
        counter += newTime - oldTime
        if newTime - sfxStartTime > sfxLength:
            p.stop()
        adc.write_byte(33, 128)
        knob = adc.read_word_data(33, 0)
        knob = ((knob & 15) << 8 | knob >> 8) - 683
        if knob < 0: knob = 0
        elif knob > 2730: knob = 2730
        Player0Bat = HEIGHT - int(round(knob * (HEIGHT - Player0Height) / 2731.)) - Player0Height
        if sorry:
            knob = adc.read_byte_data(36,0) - 9
            if knob < 0: knob = 0
            elif knob > 220: knob = 220
            Player1Bat = HEIGHT - int(round(knob * (HEIGHT - Player1Height) / 220.)) - Player1Height
            gpio.output(17, 1)
            gpio.output(17, 0)
        sorry = not sorry
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
                    p.ChangeFrequency(N_SCORE)
                    p.start(50)                    
                    Serving = True
                    ServeCount = (ServeCount + 1) % 10
                    if BallX == 0: Player1Score += 1
                    else: Player0Score += 1

                    BallXSpeed = 1 if ServeCount < 5 else -1
                    for i in range(1, 19):
                        glow.led(i, 255)
                        sleep(.05)
                    p.ChangeFrequency(N_SCORE+200)
                    for i in range(18, 0, -1):
                        glow.led(i, 0)
                        sleep(.05)
                if BallX == 2 and 0 <= BallY - Player0Bat < Player0Height or BallX == WIDTH - 3 and 0 <= BallY - Player1Bat < Player1Height:
                    N_BOUNCE = abs(N_BOUNCE - 1500)
                    p.ChangeFrequency(N_BOUNCE)
                    p.start(50)
                    sfxStartTime = time()
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
        if 10 in (Player0Score, Player1Score): break
        gpio.output(LEDS[8 * BallX / (WIDTH + 1)], True)
        currentBugger = bugger()
        output()
        oldBugger = currentBugger
        cereal.flush()
        oldTime = newTime
if Player0Score == 10: print 'Player 1 Wins!!!'
else: print 'Player 2 Wins!!!'
