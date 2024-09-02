import base64
import os
import requests

l_flag = len('flag_len_or_random')


def decode_log(log_text):
    return base64.b64decode(log_text).decode("utf-8")


def recover_flag():
    s = requests.Session()
    s.post("http://176.114.65.9:20762/register", data={"username": "rando1m", "password": "random"})
    logs_resp = s.get("http://176.114.65.9:20762/export_logs")
    ctr_user1 = 0
    ctr_user2 = 0
    logs = logs_resp.json()

    first_half = []
    second_half = []

    for log in logs:
        decoded_text = decode_log(log["text"])

        if log["user"] == "CrabbyMcGullface":
            if (
                ctr_user1 % 101 == 0
            ):
                flag_index = ctr_user1 // 101
                if flag_index < l_flag:
                    if flag_index < l_flag // 2:
                        first_half.append(decoded_text)
            ctr_user1 += 1

        elif log["user"] == "PinchySeagull":
            if (
                ctr_user2 % 48 == 0
            ):
                flag_index = ctr_user2 // 48
                if flag_index < l_flag // 2:
                    second_half.append(decoded_text)
            ctr_user2 += 1

    first_half_string = "".join(first_half)
    second_half_string = "".join(second_half)

    complete_flag = first_half_string + second_half_string

    print(f"Recovered flag: {complete_flag}")


if __name__ == "__main__":
    recover_flag()
