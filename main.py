from SessionController import SessionController
from User import User

user = User(0, "test", "test", "test@test.com", "test", "czy test")

session = SessionController(user)

print(session.check_password(user.login, "tescikowo"))

session.close()
