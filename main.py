from serial import Serial

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
'\033[2;{0}H\033[47m   \033[3;{0}H\033[47m  \033[40m \033[4;{0}H   \033[5;{0}H \033[40m  \033[6;{0}H\033[47m   ',
'\033[2;{0}H\033[47m   \033[3;{0}H\033[40m  \033[47m \033[4;{0}H   \033[5;{0}H\033[40m  \033[47m \033[6;{0}H   ',
'\033[2;{0}H \033[40m \033[47m \033[3;{0}H \033[40m \033[47m \033[3;{0}H   \033[5;{0}H\033[40m  \033[47m \033[6;{0}H\033[40m  \033[47m ',
'\033[2;{0}H\033[47m   \033[3;{0}H \033[40m  \033[4;{0}H\033[47m   \033[5;{0}H\033[40m  \033[47m \033[6;{0}H   ',
'',
'',
'',
'',
'')

WIDTH = 80
HEIGHT = 20

Player0Score = 0
Player1Score = 0

def cursor(x, y):
    write('\033[' + str(y) + ';' + str(x) + 'H')

with Serial('/dev/ttyAMA0') as cereal:
    write = cereal.write
    write(BLACK)
    write(WIDTH * HEIGHT * ' ')
    while True:
        write(SCORES[Player0Score].format(30))
        write(SCORES[Player1Score].format(48))
        cereal.flush()
