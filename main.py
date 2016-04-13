from serial import Serial
from time import time

BLACK = '\033[40m'
RED = '\033[41m'
GREEN = '\033[42m'
YELLOW = '\033[43m'
BLUE = '\033[44m'
MAGENTA = '\033[45m'
CYAN = '\033[46m'
WHITE = '\033[47m'

SCORES = (
'\033[2;{0}H\033[47m   \033[3;{0}H \033[40m \033[47m \033[4;{0}H \033[40m \033[47m \033[5;{0}H \033[40m \033[47m \033[6;{0}H   ',
'\033[2;{0}H\033[40m  \033[47m \033[3;{0}H\033[40m  \033[47m \033[4;{0}H\033[40m  \033[47m \033[5;{0}H\033[40m  \033[47m \033[6;{0}H\033[40m  \033[47m ',
'\033[2;{0}H\033[47m   \033[3;{0}H\033[40m  \033[47m \033[4;{0}H   \033[5;{0}H \033[40m  \033[6;{0}H\033[47m   ',
'\033[2;{0}H\033[47m   \033[3;{0}H\033[40m  \033[47m \033[4;{0}H   \033[5;{0}H\033[40m  \033[47m \033[6;{0}H   ',
'\033[2;{0}H\033[47m \033[40m \033[47m \033[3;{0}H \033[40m \033[47m \033[4;{0}H   \033[5;{0}H\033[40m  \033[47m \033[6;{0}H\033[40m  \033[47m ',
'\033[2;{0}H\033[47m   \033[3;{0}H \033[40m  \033[4;{0}H\033[47m   \033[5;{0}H\033[40m  \033[47m \033[6;{0}H   ',
'\033[2;{0}H\033[47m   \033[3;{0}H \033[40m  \033[4;{0}H\033[47m   \033[5;{0}H \033[40m \033[47m \033[6;{0}H   ',
'\033[2;{0}H\033[47m   \033[3;{0}H\033[40m  \033[47m \033[4;{0}H\033[40m  \033[47m \033[5;{0}H\033[40m  \033[47m \033[6;{0}H\033[40m  \033[47m ',
'\033[2;{0}H\033[47m   \033[3;{0}H \033[40m \033[47m \033[4;{0}H   \033[5;{0}H \033[40m \033[47m \033[6;{0}H   ',
'\033[2;{0}H\033[47m   \033[3;{0}H \033[40m \033[47m \033[4;{0}H   \033[5;{0}H\033[40m  \033[47m \033[6;{0}H\033[40m  \033[47m ')

NET = '\033[3;40H\033[47m \033[4;40H \033[7;40H \033[8;40H \033[11;40H \033[12;40H \033[15;40H \033[16;40H \033[19;40H \033[20;40H '

WIDTH = 80
HEIGHT = 20

oldTime = time()

Player0Score = 0
Player1Score = 0
Player0OldBat = 9
Player1OldBat = 9
Player0Bat = 9
Player1Bat = 9

def cursor(x, y):
    write('\033[' + str(y) + ';' + str(x) + 'H')

def bat(x, y):
    write('\033[40m')
    for i in range(5):
        write('\033[' + str(y + i) + ';' + str(x) + 'H ')
    write('\033[47m')
    for i in range(3):
        write('\033[' + str(y + i) + ';' + str(x) + 'H ')

with Serial('/dev/ttyAMA0') as cereal:
    write = cereal.write
    write('\033[?25l')
    write(BLACK)
    write(WIDTH * HEIGHT * ' ')
    write(NET)
    write(SCORES[Player0Score].format(30))
    write(SCORES[Player1Score].format(48))
    while True:
        newTime = time()
        print 1/(newTime - oldTime)
        bat(3, Player0Bat)
        bat(77, Player1Bat)
        cereal.flush()
        oldTime = newTime
