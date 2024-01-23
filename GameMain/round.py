from tkinter import messagebox

import pygame

from GameMain import mainboard_ui
import mglobals
import utils
from GameMain.round_ended_window import RoundEndedInfo
from Player.player import Player
from BoardDao import BoardDao

def roll():
    val = mglobals.DICEOBJ.roll_dice()
    return val

def check_round_hierarchy(players, currentplayer):
    for player in players:
        if player.round_number < currentplayer.round_number:
            can_roll = False
            break
        else:
            can_roll = True
    return can_roll

def has_round_ended(players):
    # Check if all players have the same round_number
    if all(player.round_number == players[0].round_number for player in players):
        return True
    else:
        return False


def get_players_who_need_to_roll(players, currentplayer):
    players_to_roll = "musi rzucić jeszcze:"
    player_names = []
    for player in players:
        if player.round_number < currentplayer.round_number:
            player_names.append(str(player.player_name))
    players_to_roll += ", ".join(player_names)

    return players_to_roll

def round_loop(login, user_id):

    mglobals.init()
    mainboard_ui.init_dice()
    mainboard_ui.init_printui(login)
    utils.draw_board()
    dao = BoardDao()
    num_of_players = dao.get_user_count()
    player_data = dao.get_all_players()

    players = []
    for i in range(0, num_of_players):
        player = Player(player_data[i]['user_login'],
                        player_data[i]['board_position'], player_data[i]['avatar_img'], user_id, player_data[i]['round_number'])
        players.append(player)
        mglobals.PLAYER_OBJ[player_data[i]['user_login']] = players[i]
        players[i].pm.set_starting_position()
        if players[i].player_name == login:
            currentplayer = players[i]

# Setting player info box
    mglobals.PLAYER_NAME_SPRITE[currentplayer.player_name].set_x_y(350, 120)
    mglobals.CURRENTPLAYER_IMG[currentplayer.player_name].set_x_y(480, 115)

    can_roll = check_round_hierarchy(players, currentplayer)
    ended = True

    while True:
        info = has_round_ended(players)
        if info and ended:
            number = currentplayer.round_number
            round_info = RoundEndedInfo(number)
            round_info.display_info()
            mglobals.init()
            mainboard_ui.init_dice()
            mainboard_ui.init_printui(login)
            utils.draw_board()
            dao = BoardDao()
            num_of_players = dao.get_user_count()
            player_data = dao.get_all_players()

            players = []
            for i in range(0, num_of_players):
                player = Player(player_data[i]['user_login'],
                                player_data[i]['board_position'], player_data[i]['avatar_img'], user_id,
                                player_data[i]['round_number'])
                players.append(player)
                mglobals.PLAYER_OBJ[player_data[i]['user_login']] = players[i]
                players[i].pm.set_starting_position()
                if players[i].player_name == login:
                    currentplayer = players[i]

            # Setting player info box
            mglobals.PLAYER_NAME_SPRITE[currentplayer.player_name].set_x_y(350, 120)
            mglobals.CURRENTPLAYER_IMG[currentplayer.player_name].set_x_y(480, 115)
            ended = False

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
                    currentplayer.round_number += 1
                    dao.update_player_round(login, currentplayer.round_number)
                    for player in players:
                        if player.player_name != login:
                            player.pm.render()
                    can_roll = check_round_hierarchy(players, currentplayer)
                elif event.key == pygame.K_d and can_roll == False:
                    mess = get_players_who_need_to_roll(players, currentplayer)
                    messagebox.showinfo("Character Selection", f"Nie twoja kolej, {mess}!")

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