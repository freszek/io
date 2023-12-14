import pygame

import mainboard_ui
import mglobals
import utils
from player import Player

def roll():
    val = mglobals.DICEOBJ.roll_dice()
    return val
def round_loop():

    mainboard_ui.init_dice()
    mainboard_ui.init_printui()
    utils.draw_board()
    P1 = Player(mglobals.PLAYER_ONE)
    P2 = Player(mglobals.PLAYER_TWO)

    mglobals.PLAYER_OBJ[mglobals.PLAYER_ONE] = P1
    mglobals.PLAYER_OBJ[mglobals.PLAYER_TWO] = P2

# Setting players on start
    P1.pm.render()
    P2.pm.render()

# Setting player info box
    currentplayer, otherplayer = P1, P2
    mglobals.PLAYER_NAME_SPRITE[currentplayer.player_name].set_x_y(350, 120)
    mglobals.CURRENTPLAYER_IMG[currentplayer.player_name].set_x_y(480, 115)

    can_roll, double = True, False

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
            elif event.type == pygame.KEYDOWN:
                # Dice roll
                if event.key == pygame.K_d and can_roll:
                    utils.draw_board()
                    mglobals.DICEOBJ.hide()
                    currentplayer.ps.hide()
                    val = roll()
                    currentplayer.pm.advance(val)
                    otherplayer.pm.render()
                    can_roll = False

                # Next player move
                elif event.key == pygame.K_n:
                        utils.draw_board()
                        currentplayer.pm.render()
                        otherplayer.pm.render()
                        if can_roll:
                            pass
                        else:
                            can_roll = True
                            currentplayer, otherplayer = otherplayer, currentplayer
                            mglobals.DICEOBJ.hide()
                            mglobals.PLAYER_NAME_SPRITE[currentplayer.player_name].set_x_y(350, 120)
                            mglobals.PLAYER_NAME_SPRITE[otherplayer.player_name].unset_x_y()
                            mglobals.CURRENTPLAYER_IMG[currentplayer.player_name].set_x_y(480, 115)
                            mglobals.CURRENTPLAYER_IMG[otherplayer.player_name].unset_x_y()
                            currentplayer.ps.hide()
                            otherplayer.ps.hide()

        mglobals.DICE_DISPLAY.update()
        mglobals.DICE_DISPLAY.draw(mglobals.GD)
        mglobals.CENTRE_DISPLAYS.update()
        mglobals.CENTRE_DISPLAYS.draw(mglobals.GD)
        mglobals.PLAYER_NAME_DISPLAY.update()
        mglobals.PLAYER_NAME_DISPLAY.draw(mglobals.GD)

        pygame.display.update()
        mglobals.CLK.tick(30)

        mglobals.DICE_DISPLAY.update()
        mglobals.DICE_DISPLAY.draw(mglobals.GD)
        mglobals.CENTRE_DISPLAYS.update()
        mglobals.CENTRE_DISPLAYS.draw(mglobals.GD)
        mglobals.PLAYER_NAME_DISPLAY.update()
        mglobals.PLAYER_NAME_DISPLAY.draw(mglobals.GD)

        pygame.display.update()
        mglobals.CLK.tick(30)