from tkinter import messagebox

import pygame
from GameMain import mainboard_ui
import mglobals
import utils
from GameMain.RoundDao import RoundDao
from GameMain.round_ended_window import RoundEndedInfo
from Player.player import Player
from BoardDao import BoardDao
from time_manager import TimeManager
from game_ended import GameEndedChecker


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
    if all(player.round_number != 0 for player in players):
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
    game_ended_checker = GameEndedChecker()
    mainboard_ui.init_dice()
    mainboard_ui.init_printui(login)
    utils.draw_board()
    dao = BoardDao()
    round_dao = RoundDao()
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

    time_manager = TimeManager(round_dao.get_all_rounds()[round_dao.get_highest_round_number()]['time_started'], (1000, 30))

    # Setting player info box
    mglobals.PLAYER_NAME_SPRITE[currentplayer.player_name].set_x_y(350, 120)
    mglobals.CURRENTPLAYER_IMG[currentplayer.player_name].set_x_y(480, 115)

    can_roll = check_round_hierarchy(players, currentplayer)
    while True:
        if currentplayer.round_number > 0:
            ended = round_dao.get_round_by_number(currentplayer.round_number-1)['displayed']
        else:
            ended = True
        time_manager.render_time(mglobals.GD)
        time_manager.render_round_info(mglobals.GD, round_dao.get_highest_round_number())
        info = has_round_ended(players)
        if info and not ended:
            number = currentplayer.round_number
            # Check if the game has ended
            game_ended_checker.check_game_ended(round_dao.get_highest_round_number())
            if game_ended_checker.has_game_ended():
                round_dao.end_round(number - 1)
                game_ended_checker.thank_you_menu()
            else:
                round_info = RoundEndedInfo(number-1)
                round_info.display_info()
                mglobals.init()
                mainboard_ui.init_dice()
                mainboard_ui.init_printui(login)
                utils.draw_board()
                dao = BoardDao()
                num_of_players = dao.get_user_count()
                player_data = dao.get_all_players()
                round_dao.end_round(number - 1)
                round_dao.start_round(number)
                time_manager.update_round(round_dao.get_all_rounds()[currentplayer.round_number]['time_started'])

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
                    can_roll = check_round_hierarchy(players, currentplayer)
                    for player in players:
                        if player.player_name != currentplayer.player_name:
                            player.pm.set_starting_position()
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
