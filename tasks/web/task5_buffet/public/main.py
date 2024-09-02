import hashlib

users_db = {
    "user1": hashlib.md5(b"user1_password").hexdigest(),  # b4ca6e90dcef1196a20930c2d9ecfbc0
    "user2": hashlib.md5(b"user2_password").hexdigest(),  # 049914ab3268e59eb90526f64a5322d9
    "admin": float(hashlib.md5(PASSWORD).hexdigest()),  # 0e******************************
}


def check_credentials(username, password):
    try:
        hashed_password = float(hashlib.md5(password.encode()).hexdigest())
        if username in users_db and users_db[username] == hashed_password:
            return True
        return False
    except ValueError:
        return False


def is_admin(user_input, pass_input):
    if check_credentials(user_input, pass_input):
        return "Добро пожаловать, администратор!"
    return "Доступ запрещен."


user_input = input("Введите имя пользователя: ")
pass_input = input("Введите пароль пользователя: ")
print(is_admin(user_input, pass_input))
