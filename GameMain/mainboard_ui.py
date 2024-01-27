import pygame
import mglobals
from GameMain import dice


class DiceUI(pygame.sprite.Sprite):
    def __init__(self, number1):
        super(DiceUI, self).__init__()
        self.number1 = number1
        textfont = pygame.font.Font('GameMain/monaco.ttf', mglobals.fontsize_map['mid'])
        self.image = textfont.render('You rolled : %d' % self.number1,
                                     False, mglobals.color_map['black'])
        self.rect = self.image.get_rect()
        self.unset_x_y()

    def set_x_y(self):
        self.x, self.y = 280, 500

    def unset_x_y(self):
        self.x, self.y = 900, 900

    def update(self):
        self.rect.x, self.rect.y = self.x, self.y


def init_dice():
    mglobals.DICEOBJ = dice.Dice()
    for number1 in range(1, 7):
        temp = DiceUI(number1)
        mglobals.DICE_DISPLAY.add(temp)
        mglobals.DICE_NUMBER_MAP[number1] = temp


class PRINTUI(pygame.sprite.Sprite):
    def __init__(self, message="", color='black', fntsize='small_p', alias=False):
        super(PRINTUI, self).__init__()
        self.message = message
        self.color = mglobals.color_map[color]
        self.fntsize = mglobals.fontsize_map[fntsize]
        self.alias = alias
        textfont = pygame.font.Font('GameMain/monaco.ttf', self.fntsize)
        self.image = textfont.render(self.message, self.alias, self.color)
        self.rect = self.image.get_rect()
        self.unset_x_y()

    def set_x_y(self, x=120, y=600):
        self.x, self.y = x, y

    def unset_x_y(self):
        self.x, self.y = 900, 900

    def update(self):
        self.rect.x, self.rect.y = self.x, self.y

def init_printui(login):
    color = mglobals.PLAYER_ONE_COLOR  # Assuming one player always uses PLAYER_ONE_COLOR
    temp_p = PRINTUI(login, color, 'mid', True)
    mglobals.PLAYER_NAME_DISPLAY.add(temp_p)
    mglobals.PLAYER_NAME_SPRITE[login] = temp_p
    temp = PRINTUI()
    temp.image = mglobals.P1_IMG
    mglobals.PLAYER_NAME_DISPLAY.add(temp)
    mglobals.CURRENTPLAYER_IMG[login] = temp