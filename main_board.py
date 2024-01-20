import pygame

import mglobals
import round
from game_rules import GameRulesApp
from player_avatar import PlayerAvatar
import os


def display_rules():
    # showing game rules
    app = GameRulesApp()
    app.run()


def main(players):
    mglobals.init()
    # showing game rules
    display_rules()
    # handling choosing player color
    player_selector = PlayerAvatar(mglobals.DISPLAY_W, mglobals.DISPLAY_H, 6)
    selected_player_avatar = player_selector.choose_player()
    mglobals.PLAYER_IMG.append(pygame.image.load(selected_player_avatar))
    pictures = [el for el in os.listdir(os.getcwd() + '/pics') if el != 'board.jpg'
                and el != selected_player_avatar.split('/')[1]]
    if isinstance(players, list):
        for i in range(1, len(players)):
            mglobals.PLAYER_IMG.append(pygame.image.load('pics/' + pictures[i]))
    else:
        print("Zły format gracza")

    round.round_loop(players)
    pygame.quit()
    quit()
