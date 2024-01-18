import pygame

import mglobals
import round
from GameMain.game_rules import GameRulesApp
from Player.player_avatar import PlayerAvatar


def display_rules():
    # showing game rules
    app = GameRulesApp()
    app.run()

def main():
    mglobals.init()
    # showing game rules
    display_rules()
    # handling choosing player color
    player_selector = PlayerAvatar(mglobals.DISPLAY_W, mglobals.DISPLAY_H, 6)
    selected_player_avatar = player_selector.choose_player()
    mglobals.P1_IMG = pygame.image.load(selected_player_avatar)
    mglobals.P2_IMG = pygame.image.load('GameMain/pics/p2.png')

    round.round_loop()
    pygame.quit()
    quit()


if __name__ == '__main__':
    main()
