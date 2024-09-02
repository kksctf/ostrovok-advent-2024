import os
import random
import string
from datetime import datetime

from ext import db
from models import Log, User
from routes import encode_log

flag = r'CTF{EXAMPLE}' if 'FLAG' not in os.environ else os.environ['FLAG'].replace('"', '')


def generate_password(length=12):
    characters = string.ascii_letters + string.digits + string.punctuation
    return ''.join(random.choice(characters) for _ in range(length))


def generate_note_text(length=50):
    words = ["loRem", "ips4m", "dolor", "sit", "a0et", "cons8ctetur", "ad[piscing", "elit", "sed", "d3o",
             "eI{usmod", "t}Cmpor", "incidaAdunt", "ut", "laboVe", "et", "do$0ore", "maglna", "ali01qua"]
    return ' '.join(random.choice(words) for _ in range(length))


def generate_log_action():
    actions = [
        "Logged in", 
        "Logged out", 
        "Viewed note", 
        "Added a note", 
        "Deleted a note", 
        "Edited a note"
    ]
    return random.choice(actions)


def create_users_notes_logs():
    users_data = [
        {"username": "CrabbyMcGullface", "password": generate_password()},
        {"username": "PinchySeagull", "password": generate_password()},
        {"username": "ClawtasticChirp", "password": generate_password()},
        {"username": "GullGoneCrabby", "password": generate_password()},
        {"username": "SnappyWings", "password": generate_password()},
        {"username": "BeakyMcCrabster", "password": generate_password()},
    ]

    mid_index = len(flag) // 2
    first_half = flag[:mid_index]
    second_half = flag[mid_index:]

    user_first_half = users_data[0]
    user_second_half = users_data[1]

    for index, user_data in enumerate(users_data):
        new_user = User(username=user_data["username"])
        new_user.set_password(user_data["password"])
        db.session.add(new_user)
        db.session.commit()

        num_logs = random.randint(10000, 20000)
        for i in range(num_logs):
            log_action = generate_log_action()

            if user_data == user_first_half and i % 101 == 0:
                flag_index = i // 101
                if flag_index < len(first_half):
                    log_text = first_half[flag_index]
                else:
                    log_text = generate_note_text()
            elif user_data == user_second_half and i % 48 == 0:
                flag_index = i // 48
                if flag_index < len(second_half):
                    log_text = second_half[flag_index]
                else:
                    log_text = generate_note_text()
            else:
                log_text = generate_note_text()

            log_entry = Log(user_id=new_user.id, action=log_action, timestamp=datetime.utcnow(), text=encode_log(log_text))
            db.session.add(log_entry)

    db.session.commit()
    print("База данных успешно заполнена.")