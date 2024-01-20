import pygame

from GameMain import mainboard_ui
import mglobals
import utils
from Player.player import Player
from BoardDao import BoardDao

def roll():
    val = mglobals.DICEOBJ.roll_dice()
    return val

def round_loop(login, user_id):

    mainboard_ui.init_dice()
    mainboard_ui.init_printui(login)
    utils.draw_board()
    dao = BoardDao()
    num_of_players = dao.get_user_count()
    current_p_p = dao.get_board_entry_by_user_login(login)['board_position']
    player_data = dao.get_all_players()
    # P1 = Player(login, current_p_p)
    # P2 = Player(mglobals.PLAYER_TWO, 0)

    players = []
    for i in range(0, num_of_players):
        player = Player(player_data[i]['user_login'], player_data[i]['board_position'], player_data[i]['id'])
        players.append(player)
        mglobals.PLAYER_OBJ[player_data[i]['user_login']] = players[i]
        players[i].pm.set_starting_position()
        if players[i].player_name == login:
            currentplayer = players[i]

# Setting player info box
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
                #   otherplayer.pm.render()
                    can_roll = False

                # Next player move
                elif event.key == pygame.K_n:
                        # utils.draw_board()
                        # currentplayer.pm.render()
                        # otherplayer.pm.render()
                        # if can_roll:
                        #     pass
                        # else:
                        #     can_roll = True
                        #     currentplayer, otherplayer = otherplayer, currentplayer
                        #     mglobals.DICEOBJ.hide()
                        #     mglobals.PLAYER_NAME_SPRITE[currentplayer.player_name].set_x_y(350, 120)
                        #     mglobals.PLAYER_NAME_SPRITE[otherplayer.player_name].unset_x_y()
                        #     mglobals.CURRENTPLAYER_IMG[currentplayer.player_name].set_x_y(480, 115)
                        #     mglobals.CURRENTPLAYER_IMG[otherplayer.player_name].unset_x_y()
                        #     currentplayer.ps.hide()
                        #     otherplayer.ps.hide()
                    pygame.quit()

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