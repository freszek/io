from datetime import timedelta, datetime

import pygame
import sys
import mglobals
import round
from BoardDao import BoardDao
from GameMain.time_manager import TimeManager
from RoundDao import RoundDao
from User.UserDao import UserDao


def main():
    current_user_login = str(sys.argv[1])
    current_user_id = int(sys.argv[2])
    print(current_user_login)
    mglobals.init()
    dao = BoardDao()
    round_dao = RoundDao()
    user_dao = UserDao()
    selected_player_avatar = dao.get_board_entry_by_user_login(current_user_login)['avatar_img']
    mglobals.P1_IMG = pygame.image.load(selected_player_avatar)

# adding game started time to count round times
    if not round_dao.get_all_rounds():
        round_dao.start_round(round_number=0)
# checking if round time ended
    current_number = round_dao.get_highest_round_number()
    current_round = round_dao.get_round_by_number(current_number)['time_started']
    print(current_round)
    time_manager = TimeManager(current_round, (1000, 30))
    if time_manager.get_time_left() <= timedelta(seconds=0):
        print("Round ended")
        users_to_update = dao.get_users_with_current_round(current_number)
        current_date = datetime.now().strftime('%Y-%m-%d')
        for user in users_to_update:
            dao.update_player_round(user, current_number+1)
            id = dao.get_board_entry_by_user_login(user)['id']
            user_dao.add_points(user_id=id, points=0, date=current_date, category_name="did not roll")
#############################################################################################################
# checking if new players joined the game
    difference = abs(dao.get_highest_round_number()-dao.get_board_entry_by_user_login(current_user_login)['round_number'])
    if difference >= 2:
        dao.update_player_round(current_user_login, dao.get_highest_round_number())
        id = dao.get_board_entry_by_user_login(current_user_login)['id']
        current_date = datetime.now().strftime('%Y-%m-%d')
        for i in range(0, difference):
            user_dao.add_points(user_id=id, points=0, date=current_date, category_name="was not in game")
        print("Round updated")
    round.round_loop(current_user_login, current_user_id)
    pygame.quit()
    quit()


if __name__ == '__main__':
    main()
