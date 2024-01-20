import pygame
import mainboard_ui
import mglobals
import utils
from player import Player


def roll():
    val = mglobals.DICEOBJ.roll_dice()
    return val


def round_loop(user_data=None):
    mainboard_ui.init_dice()
    mainboard_ui.init_printui([el['login'] for el in user_data])
    utils.draw_board()
    players = []

    for i, el in enumerate(user_data):
        player = Player(el['login'], i)
        mglobals.PLAYER_OBJ[el['login']] = player

        # Setting players on start
        player.pm.render()
        players.append(player)

    # Setting player info box
    index = 0
    players_num = len(players)
    currentplayer = players[index]
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
                    for player in players:
                        if player != currentplayer:
                            player.pm.render()
                    can_roll = False

                # Next player move
                elif event.key == pygame.K_n:
                    utils.draw_board()
                    for player in players:
                        player.pm.render()
                    if not can_roll:
                        can_roll = True
                        index += 1
                        if index == players_num:
                            index = 0
                        currentplayer = players[index]
                        mglobals.DICEOBJ.hide()
                        mglobals.PLAYER_NAME_SPRITE[currentplayer.player_name].set_x_y(350, 120)
                        mglobals.CURRENTPLAYER_IMG[currentplayer.player_name].set_x_y(480, 115)
                        for player in players:
                            if player != currentplayer:
                                mglobals.PLAYER_NAME_SPRITE[player.player_name].unset_x_y()
                                mglobals.CURRENTPLAYER_IMG[player.player_name].unset_x_y()

        mglobals.DICE_DISPLAY.update()
        mglobals.DICE_DISPLAY.draw(mglobals.GD)
        mglobals.CENTRE_DISPLAYS.update()
        mglobals.CENTRE_DISPLAYS.draw(mglobals.GD)
        mglobals.PLAYER_NAME_DISPLAY.update()
        mglobals.PLAYER_NAME_DISPLAY.draw(mglobals.GD)

        pygame.display.update()
        mglobals.CLK.tick(30)
