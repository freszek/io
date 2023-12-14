
import random

import mglobals

class Dice(object):
    def __init__(self):
        self.number1 = 1
        self.dicemap = mglobals.DICE_NUMBER_MAP

    def roll_dice(self):
        self.number1 = random.randrange(1, 7)
        self.show()
        return self.number1

    def show(self):
        self.dicemap[self.number1].set_x_y()

    def hide(self):
        self.dicemap[self.number1].unset_x_y()

