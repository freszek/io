
import pygame
import collections

DISPLAY_W, DISPLAY_H = 1200, 800
BOARD_WIDTH = 800

BOARD_SQUARES = 40

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

BROWN = (165, 42, 42)
PURPLE = (128, 0, 128)
BLUE = (0, 0, 255)
SKY_BLUE = (576, 226, 255)
DEEP_SKY_BLUE = (0, 191, 255)
DARK_BLUE = (0, 0, 139)
ROYAL_BLUE = (65, 105, 225)
PINK = (255, 0, 255)
ORANGE = (255, 140, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
DARKER_YELLOW = (200, 160, 30)
GREEN = (0, 255, 0)
SEA_GREEN = (46, 139, 87)
GRAY = (169, 169, 169)

PLAYER_TWO = 'Player 2'

PLAYER_ONE_COLOR = 'royal_blue'
PLAYER_TWO_COLOR = 'sea_green'

color_map = {
        'purple': PURPLE,
        'black': BLACK,
        'brown': BROWN,
        'sky blue': DEEP_SKY_BLUE,
        'pink': PINK,
        'orange': ORANGE,
        'red': RED,
        'yellow': DARKER_YELLOW,
        'green': GREEN,
        'blue': BLUE,
        'sea_green': SEA_GREEN,
        'royal_blue': ROYAL_BLUE,
        'white': WHITE,
        'gray': GRAY,
}

fontsize_map = {
        'big': 50,
        'mid': 25,
        'small_p': 15,
        'small': 12,
}

GD = None
CLK = None
BACK_IMG = None
P1_IMG = None
P_INFO_CLRSCR = None
MSG_CLRSCR = None
MSG_SCR = None

PLAYER_OBJ = {}
PLAYER_NAME_SPRITE = {}
CURRENTPLAYER_IMG = {}
PLAYER_NAME_DISPLAY = pygame.sprite.Group()

DICEOBJ = None
DICE_NUMBER_MAP = {}
DICE_DISPLAY = pygame.sprite.Group()

PROPERTY_NAME_SPRITE_MAP = {}
PROPERTY_DISPLAYS = pygame.sprite.Group()
CENTRE_DISPLAYS = pygame.sprite.Group()
POBJECT_MAP = {}
PNAME_OBJ_MAP = {}
PROP_COLOR_INDEX = collections.defaultdict(list)
INDEX_PROPPIC_MAP = {}


def load_imgs():
    global BACK_IMG, P1_IMG, P_INFO_CLRSCR, MSG_CLRSCR
    BACK_IMG = pygame.image.load('GameMain/pics/board.jpg')
    BACK_IMG = pygame.transform.scale(BACK_IMG, (DISPLAY_W - 400, DISPLAY_H))
    P_INFO_CLRSCR = pygame.Surface([380, 380])
    MSG_CLRSCR = pygame.Surface([380, 18])

def init_pygame():
    global GD, CLK
    pygame.init()
    GD = pygame.display.set_mode((DISPLAY_W, DISPLAY_H))
    pygame.display.set_caption('Green Game')
    CLK = pygame.time.Clock()
    pygame.event.set_allowed([pygame.QUIT, pygame.KEYDOWN, pygame.KEYUP])

def init():
    init_pygame()
    load_imgs()