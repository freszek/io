import mglobals
from GameMain.BoardDao import BoardDao
from User.UserDao import UserDao
from User.Userr import Userr as User


class SessionController:
    def __init__(self):
        self.session_user = None
        self.user_dao = UserDao()
        self.board_dao = BoardDao()
        self.counter = 0

    def register(self, login, password, email, answer, question):
        if self.check_login(login):
            print("Uzytkownik o tym loginie juz istnieje!")
            return

        user = User(0, login, password, email, question, answer)
        self.session_user = user
        self.user_dao.create_user(user)
        self.create_board_table_in_DB()
        print(f"ZAREJESTROWANY {login}")

    def check_login(self, login: str) -> bool:
        users = self.user_dao.get_all()
        return any(user.login == login for user in users)

    def check_password(self, login: str, password: str) -> bool:
        user = self.user_dao.get_by_login(login)
        if user:
            hashed_password = self.user_dao.hash_password(password)
            return user.password == hashed_password
        return False

    def log_in(self, login: str, password: str, answer: str) -> bool:
        if answer != "":
            if self.check_login(login) and self.check_answer(login, answer):
                print("ZALOGOWANY")
                self.session_user = self.user_dao.get_by_login(login)
                self.session_user.is_logged = True
                return True

        else:
            if self.check_login(login) and self.check_password(login, password):
                print("ZALOGOWANY")
                self.session_user = self.user_dao.get_by_login(login)
                self.session_user.is_logged = True
                print(self.session_user.id)
                return True
        print("Niezalogowany")
        return False

    def create_board_table_in_DB(self) -> bool:
        self.board_dao.add_board_entry(
            user_login=self.session_user.login,
            board_position=0,
            avatar_img=mglobals.default,
            round_number=0
        )

    def check_if_logged(self) -> bool:
        return self.session_user.is_logged

    def check_answer(self, login: str, answer: str) -> bool:
        user = self.user_dao.get_by_login(login)
        return user.answer == answer

    def log_out(self, login: str):
        user = self.user_dao.get_by_login(login)
        if user:
            user.is_logged = False

    def delete_user(self, password: str) -> bool:
        print(self.session_user)
        if self.check_password(self.session_user.login, password):
            self.user_dao.delete_user(self.session_user)
            self.log_out(self.session_user.login)
            return True
        return False

    def change_password(self, current_password: str, new_password: str) -> bool:
        if self.check_password(self.session_user.login, current_password):
            self.user_dao.update_user(self.session_user, new_password)
            return True
        return False

    def close(self):
        self.user_dao.close()