from UserDao import *


class SessionController:
    def __init__(self, user: User):
        self.session_user = user
        self.user_dao = UserDao()

    def check_login(self, login: str) -> bool:
        users = self.user_dao.get_all()
        return any(user.login == login for user in users)

    def check_password(self, login: str, password: str) -> bool:
        user = next((user for user in self.user_dao.get_all() if self.check_login(login)), None)
        if user:
            hashed_password = self.user_dao._hash_password(password)
            return user.password == hashed_password
        return False

    def log_in(self, login: str, password: str) -> bool:
        if self.check_login(login) and self.check_password(login, password):
            self.session_user.is_logged = True
            return True
        return False

    def check_if_logged(self) -> bool:
        return self.session_user.is_logged

    def check_answer(self, login: str, answer: str, question: str) -> bool:
        user = next((user for user in self.user_dao.get_all() if self.check_login(login)), None)
        return user.answer == answer and user.question == question

    def log_out(self, login: str):
        user = next((user for user in self.user_dao.get_all() if self.check_login(login)), None)
        if user:
            user.is_logged = False
            self.user_dao.update_user(user, user.password)

    def close(self):
        self.user_dao.close()
