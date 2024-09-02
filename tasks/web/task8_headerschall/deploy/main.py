#!/usr/bin/env python

# Idea
#
# Таск на знание HTTP Headers. Таск состоит из 4 этапов:
# 1) User-agent ; Текстовый браузер Lynx
# 2) Код страны в Accept-Language. Konkani
# 3) From - Чек email адреса отеля. Положить в другом таске?
# 4) Date - отправлять мы можем только второго января, только в этот день прилетает самолёт с почтой и забирает его.
#
# Таск, чисто технически, - чистая угадайка (уцуцуга). На фронте все подсказки.
# SOLVE
# curl -XPOST 127.0.0.1:1337 -A "lynx" --header 'Content-Language: kok' --header 'From: a@a.a' --header 'Date: Tue, 2 Jan 2024 13:37:00 GMT'


from flask import Flask, request, redirect, make_response , jsonify, send_from_directory, render_template, request
import os



flag = r'CTF{EXAMPLE}' if 'FLAG' not in os.environ else os.environ['FLAG'].replace('"','')
DEBUG_VAR = True


app = Flask("task8_headersguesser",
            template_folder=".",
            static_folder="./static")


def normalize_check(header:str, param:str):
    if header != None: 
        if param in header.lower().strip():
            return True
        
    return False

@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'),
                               'favicon.ico', mimetype='image/vnd.microsoft.icon')

@app.route("/", methods=["GET", "POST"])
def index():
    ua = request.headers.get("User-Agent")
    cl = request.headers.get("Content-Language")
    fr = request.headers.get("From")
    da = request.headers.get("Date")
    
    if normalize_check(ua, "lynx"):
        if normalize_check(cl,"kok"):
            if normalize_check(fr, "@"):   # Регулярки? Какие регулярки?
                if normalize_check(da,"2 jan"):
                    if request.method == "POST":
                        return render_template("flag.html", flag=flag)
                    return render_template("index.html", stage=4)
                return render_template("index.html", stage=3)
            return render_template("index.html", stage=2)
        return render_template("index.html", stage=1)
    
    
    return render_template("index.html", stage=0)


if __name__ == "__main__":
    with app.app_context():
        app.run(host="0.0.0.0",
        port=1337,
        debug=DEBUG_VAR)
        
        
    