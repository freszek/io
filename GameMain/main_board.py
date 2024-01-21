import pygame
import sys

import mglobals
import round
from GameMain.game_rules import GameRulesApp
from Player.player_avatar import PlayerAvatar
from BoardDao import BoardDao


def display_rules():
    # showing game rules
    app = GameRulesApp()
    app.run()


def main():
    current_user_login = str(sys.argv[1])
    current_user_id = int(sys.argv[2])
    print(current_user_login)
    mglobals.init()
    dao = BoardDao()
    selected_player_avatar = dao.get_board_entry_by_user_login(current_user_login)['avatar_img']
    mglobals.P1_IMG = pygame.image.load(selected_player_avatar)
<<<<<<< HEAD
    round.round_loop(current_user_login)
=======
    mglobals.P2_IMG = pygame.image.load('GameMain/pics/p2.png')

    round.round_loop(current_user_login, current_user_id)
>>>>>>> origin/Scenariusz
    pygame.quit()
    quit()


if __name__ == '__main__':
    main()
