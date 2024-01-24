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
    round.round_loop(current_user_login, current_user_id)
    pygame.quit()
    quit()


if __name__ == '__main__':
    main()
