import random

import pygame

import mglobals
import utils
from mini_game import MiniGame
from mainEvents import game


class PlayerMovement:
    RECT_WIDTH = 65
    RECT_HEIGHT = 106
    SQ_HEIGHT_WIDTH = 106
    PIMG_WIDTH = 60
    PIMG_HEIGHT = 40


    def __init__(self, player_name, player_img, position=0):
        self.position = position
        self.player_name = player_name
        self.player_img = player_img
        self.x, self.y = 720, 730
        game1 = MiniGame(1, "WaterSafe", 30, 5)
        game2 = MiniGame(2, "CleanUp", 30, 5)
        game3 = MiniGame(3, "EkoSnake", 30, 5)
        game4 = MiniGame(4, "Snake", 30, 5)
        self.game_list = [game1, game2, game3, game4]


    def choose_mini_game(self):
        random_number = random.randint(0, 3)
        return self.game_list[random_number]


    def advance(self, count):
        currentplayer = mglobals.PLAYER_OBJ[self.player_name]
        prev_pos = self.position
        old_position = self.position
        self.position = (self.position + count) % mglobals.BOARD_SQUARES
        # if self.position == 0 or (prev_pos > self.position and \
        #                           not currentplayer.jail.in_jail):
        #     currentplayer.give_player_cash(200)
        # if self.position in infra.CHANCE_INDEXLIST + infra.CHEST_INDEXLIST:
        #     infra.ChanceChest().chance_chest(self.player_name)
        # # Income Tax deduction
        # if self.position == 4:
        #     currentplayer.take_player_cash(200)
        # # Super Tax deduction
        # elif self.position == 38:
        #     currentplayer.take_player_cash(100)
        # # Go to jail
        # elif self.position == 30:
        #     self.position = 10
        #     currentplayer.jail.in_jail = True
        self.reposition()
        self.render()

        result = 0
# =============================================================================
        if self.position != 0:
            while result < 5:
                result = self.choose_mini_game().startMinigame()
# =============================================================================
        utils.draw_board()
        self.render()
        if old_position + count >= mglobals.BOARD_SQUARES:
            game()
                 
                 
    def reposition(self):
        # If the position corresponds to a square
        if self.position % 10 == 0:
            if self.position in [0, 10]:
                self.y = mglobals.DISPLAY_H - PlayerMovement.PIMG_HEIGHT - 33
                self.x = 720 if self.position == 0 \
                    else 25
            else:
                self.y = 33
                self.x = 720 if self.position == 30 \
                    else 25

        # If the position corresponds to a vertical rectangle
        elif (self.position > 0 and self.position < 10) or \
                (self.position > 20 and self.position < 30):
            if self.position > 0 and self.position < 10:
                self.y = 730
                self.x = (mglobals.BOARD_WIDTH - PlayerMovement.SQ_HEIGHT_WIDTH
                          - PlayerMovement.PIMG_WIDTH - 3
                          - ((self.position - 1) * PlayerMovement.RECT_WIDTH))
            else:
                self.y = 33
                self.x = (PlayerMovement.SQ_HEIGHT_WIDTH + 3
                          + (((self.position % 10) - 1) * PlayerMovement.RECT_WIDTH))

        # If the position corresponds to a horizontal rectangle
        else:
            if self.position > 10 and self.position < 20:
                self.x = 25
                self.y = (mglobals.DISPLAY_H - PlayerMovement.SQ_HEIGHT_WIDTH
                          - PlayerMovement.PIMG_HEIGHT - 12
                          - (((self.position % 10) - 1) * PlayerMovement.RECT_WIDTH))
            else:
                self.x = 720
                self.y = (PlayerMovement.SQ_HEIGHT_WIDTH + 12
                          + (((self.position % 10) - 1) * PlayerMovement.RECT_WIDTH))

    def render(self):
        mglobals.GD.blit(self.player_img, (self.x, self.y))


class PlayerSelection:
    BOX_THICKNESS = 5
    RECT_WIDTH = 65
    RECT_HEIGHT = 106
    SQ_HEIGHT_WIDTH = 106

    def __init__(self, color, position=0):
        self.position = position
        self.color = color
        self.x, self.y = 0, 0
        self.cw, self.ch = 0, 0
        self.reposition()
        self.render()

    def reposition(self):
        # If the position corresponds to a square
        if self.position % 10 == 0:
            if self.position in [0, 10]:
                self.y = mglobals.DISPLAY_H - PlayerSelection.SQ_HEIGHT_WIDTH
                self.x = 0 if self.position == 10 \
                    else mglobals.BOARD_WIDTH - PlayerSelection.SQ_HEIGHT_WIDTH
            else:
                self.y = 0
                self.x = 0 if self.position == 20 \
                    else mglobals.BOARD_WIDTH - PlayerSelection.SQ_HEIGHT_WIDTH
            self.cw, self.ch = PlayerSelection.SQ_HEIGHT_WIDTH, PlayerSelection.SQ_HEIGHT_WIDTH

        # If the position corresponds to a vertical rectangle
        elif (self.position > 0 and self.position < 10) or \
                (self.position > 20 and self.position < 30):
            if self.position > 0 and self.position < 10:
                self.y = (mglobals.DISPLAY_H - PlayerSelection.RECT_HEIGHT)
                self.x = (mglobals.BOARD_WIDTH
                          - PlayerSelection.SQ_HEIGHT_WIDTH
                          - (PlayerSelection.RECT_WIDTH * self.position))
            else:
                self.y = 0
                self.x = (PlayerSelection.SQ_HEIGHT_WIDTH
                          + (PlayerSelection.RECT_WIDTH * ((self.position % 10) - 1)))
            self.cw, self.ch = PlayerSelection.RECT_WIDTH, PlayerSelection.RECT_HEIGHT

        # If the position corresponds to a horizontal rectangle
        else:
            if self.position > 10 and self.position < 20:
                self.x = 0
                self.y = (mglobals.DISPLAY_H
                          - PlayerSelection.SQ_HEIGHT_WIDTH
                          - (PlayerSelection.RECT_WIDTH * (self.position % 10)))
            else:
                self.x = mglobals.BOARD_WIDTH - PlayerSelection.SQ_HEIGHT_WIDTH
                self.y = (PlayerSelection.SQ_HEIGHT_WIDTH
                          + (PlayerSelection.RECT_WIDTH * ((self.position % 10) - 1)))
            self.ch, self.cw = PlayerSelection.RECT_WIDTH, PlayerSelection.RECT_HEIGHT

    def advance(self):
        self.position += 1
        if self.position >= mglobals.BOARD_SQUARES:
            self.position %= mglobals.BOARD_SQUARES
        self.reposition()
        self.render()

    def render(self):
        pygame.draw.rect(mglobals.GD, mglobals.color_map[self.color],
                         [self.x, self.y, self.cw, self.ch],
                         PlayerSelection.BOX_THICKNESS)

    def hide(self):
        psprite = mglobals.INDEX_PROPPIC_MAP.get(self.position, None)
        if not psprite:
            return
        psprite.unset_x_y()


class Player:
    RECT_WIDTH = 65
    SQ_HEIGHT_WIDTH = 106

    def __init__(self, player_name):
        self.player_name = player_name
        self.color = mglobals.PLAYER_ONE_COLOR \
            if self.player_name == mglobals.PLAYER_ONE \
            else mglobals.PLAYER_TWO_COLOR
        self.ps = PlayerSelection(self.color)
        self.pm = PlayerMovement(self.player_name, mglobals.P1_IMG) \
            if self.player_name == mglobals.PLAYER_ONE \
            else PlayerMovement(self.player_name, mglobals.P2_IMG)