from UserDao import *


class SessionController:
    def __init__(self):
        self.session_user = None
        self.user_dao = UserDao()

    def register(self, login, password, email, answer, question):
        user = User(0, login, password, email, question, answer)
        self.session_user = user
        self.user_dao.create_user(user)

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
                return True
        return False

    def check_if_logged(self) -> bool:
        return self.session_user.is_logged

    def check_answer(self, login: str, answer: str) -> bool:
        user = self.user_dao.get_by_login(login)
        return user.answer == answer

    def log_out(self, login: str):
        user = next((user for user in self.user_dao.get_all() if self.check_login(login)), None)
        if user:
            user.is_logged = False
            self.user_dao.update_user(user, user.password)

    def close(self):
        self.user_dao.close()
