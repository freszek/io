class User:
    def __init__(self, id, login, password, email, answer, question):
        self.id = id
        self.login = login
        self.password = password
        self.email = email
        self.is_logged = 0
        self.answer = answer
        self.question = question
