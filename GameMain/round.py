import pygame

from GameMain import mainboard_ui
import mglobals
import utils
from Player.player import Player
from BoardDao import BoardDao

def roll():
    val = mglobals.DICEOBJ.roll_dice()
    return val

def round_loop(login):

    mainboard_ui.init_dice()
    mainboard_ui.init_printui(login)
    utils.draw_board()
    dao = BoardDao()
    dao.get_board_entry_by_user_login(login)
    position = dao.get_board_entry_by_user_login(login)['board_position']
    P1 = Player(login, position)
    P2 = Player(mglobals.PLAYER_TWO,0)

    mglobals.PLAYER_OBJ[login] = P1
    mglobals.PLAYER_OBJ[mglobals.PLAYER_TWO] = P2

# Setting players on start
    P1.pm.set_starting_position()
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
                    dao.update_player_position(login, currentplayer.pm.position + val)
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