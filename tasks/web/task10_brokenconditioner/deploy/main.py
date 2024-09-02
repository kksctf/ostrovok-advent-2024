#!/usr/bin/env python

# Idea
# Крабы решили отдохнуть в новом роскошном отеле чаек на побережье. 
# Однако находчивые чайки, желая заработать больше денег, намеренно сломали кондиционер в номере крабов. 
# Управление кондиционером осуществляется через веб-приложение, и крабы заметили, что оно работает нестабильно. 
# Помогите крабам разобраться, почему кондиционер не работает, и получите секретный флаг, спрятанный в системе управления: `/etc/flag.txt`
#
# Этапы таска:
# - Перед нами какое-то проложение с API по ручке /accontrol/
# - У него есть параметры:
# -- room_number - Номер комнаты. Формат: [1-399].
# -- temp        - нужная температура. Формат: +-N C^{0}. 
# -- ac_unit     - Номер кондиционера. Формат: [0-N]
#
# - В параметрах есть классический фильтр на спецсимволы.
# -- blacklist = [";", "&", "|", "`", "$", "(", ")", "{", "}", "[", "]"]
# - А еще есть ограничение на размер внедряемых данных >:)
# - Основная задача - собрать на системе исполняемый файл и уже его исполнить через sh ./a.sh

from flask import Flask, request, redirect, make_response , jsonify, send_from_directory, render_template
import os

flag = r'CTF{EXAMPLE}' if 'FLAG' not in os.environ else os.environ['FLAG'].replace('"','')
###
f = open("/etc/flag.txt", "w")
f.write(flag)
f.close()
###
DEBUG_VAR = True




app = Flask("task10_brokenconditioner",
            template_folder=".",
            static_folder="./static")
            
def check_for_blacklist(val: str) -> bool:
    blacklist = [";", "&", "|", "`", "$", "(", ")", "{", "}", "[", "]"]
    for c in val:
        if c in blacklist:
            return False
    return True

@app.route("/")
def index():
    return redirect("/acctl")


@app.route("/acctl", methods=['GET','POST'])
def acctl():
    if request.method == "GET":
        return render_template("index.html")

    elif request.method == "POST":

        post = request.json

        
        room_id  = post["room"]
        temp     = str(post["temp"])
        ac_id    = post["ac_id"] 

        # Проверка параметра temp на размер - 3 символа (-35 -- +35 градусов). Тут нет блеклиста, тк должна вставляться ';'
        # и на фронте должен быть ползунок, мол "разработчик" решил пропустить шаг валидации тк "Ну там ползунок, а не форма"

        try:
            if len(temp) > 3:
                raise Exception("Bad Temp :: Bad len")
            
            if temp.find("+") == -1 and temp.find("-") == -1:
                raise Exception("Bad Temp :: Sign was lost")
            
        except Exception as e:
            return jsonify({"Status": str(e)})

        # Проверка room параметра на размер - 4 символа (1- 1001 комнат) + blacklist
        try:
            if not check_for_blacklist(room_id):
                raise Exception("Bad Room ID :: Failed blacklist check")
            # TODO: len check

            if len(room_id) > 4:
                raise Exception("Bad Room ID :: Too big room nuber")

        except Exception as e:
            return jsonify({"Status": str(e)})
        
        # Проверка acid параметра на размер - 8 символов + blacklist.
        try:
            if not check_for_blacklist(ac_id):
                raise Exception("Bad AC ID :: Failed blacklist check")
            # TODO: len check

            if len(ac_id) != 8:
                raise Exception("Bad AC ID :: Incorrect len of pin code")

        except Exception as e:
            return jsonify({"Status": str(e)})
    
        # TODO: os.open + возврат параметров
        cmd_res = os.popen("python3 acctl.py {} {} {}".format(temp,room_id, ac_id), 'r')
        data = cmd_res.read(100)
        # TODO: сформировать json с ответом. Там может быть либо ошибка, либо результат выполнения команды в acctl
        cmd_res.close()
        
        return jsonify({"Status":data}), 200
    else:
        return r'{"Status":"Unknown error"}', 404


if __name__ == "__main__":
    with app.app_context():
        app.run(host="0.0.0.0",
        port=1337,
        debug=DEBUG_VAR)