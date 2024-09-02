#!/usr/bin/env python

# Idea
# Просто генерится грид из картинок "С камер"
# У картинок есть id и они лежат в статике (условно 16 штук)
# id картинок - md5 от 1,2,3,4 ...
# 17 картинка, которая никогда не подгружается - флаг

# 1 c4ca4238a0b923820dcc509a6f75849b +
# 2 c81e728d9d4c2f636f067f89cc14862c -
# 3 eccbc87e4b5ce2fe28308fd9f2a7baf3 +
# 4 a87ff679a2f3e71d9181a67b7542122c +
# 5 e4da3b7fbbce2345d7772b0674a318d5 +
# 6 1679091c5a880faf6fb5e6087eb1b2dc +
# 7 8f14e45fceea167a5a36dedd4bea2543 +
# 8 c9f0f895fb98ab9159f51fd0297e236d +
# 9 45c48cce2e2d7fbdea1afc51c7c6ad26 +
# 10 d3d9446802a44259755d38e6d163e820 -
# 11 6512bd43d9caa6e02c990b0a82652dca -
# 12 c20ad4d76fe97759aa27a0c99bff6710 -
# 13 c51ce410c124a10e0db5e4b97fc2af39 -
# 14 aab3238922bcc25a6f606eb525ffdc56 -
# 15 9bf31c7ff062936a96d3c8bd1f8f2ff3 -
# 16 c74d97b01eae257e44aa9d5bade97baf -
# 17 70efdf2ec9b086079795c442636b55fb - flag

from flask import Flask, request, render_template, redirect, render_template_string, Response, url_for,send_from_directory
import os
import hashlib
import random
import string

from PIL import Image, ImageFont, ImageDraw

app = Flask("task4_cameraman",
            template_folder=".",
            static_folder="./static")

flag = r'CTF{EXAMPLE}' if 'FLAG' not in os.environ else os.environ['FLAG'].replace('"','')

DEBUG_VAR = True

def prepare_image_list(id: int):
    random.seed(id)
    id_p = [ "/static/{}.jpg".format(hashlib.md5(str(random.randint(1,16)).encode()).hexdigest()) for _ in range(16)]
    
    if DEBUG_VAR:
        print("id=",id)
        print(id_p)

    return id_p

def generate_flag_png(text):
    font = ImageFont.truetype("./static/Inconsolata-Regular.ttf", size=32)
    box = font.getbbox(text)
    square_box = (box[2], box[2])
    img = Image.new("RGB", square_box)
    draw = ImageDraw.Draw(img)
    draw_point = (0, box[2]/2)
    draw.multiline_text(draw_point, text, font=font, fill=(255,255,255), align="center")
    img.save("./static/70efdf2ec9b086079795c442636b55fb.jpg")


@app.route("/camera/<id>")
def camera_id(id=0):
    print("id=",id)
    
    try:
        id = int(id) # wtf
    except:
        return redirect("/camera/1")
    
    if id <= 0:
        return redirect("/camera/1")
    if id >= 256:
        return redirect("/camera/255")
    
    return render_template("camera_view.html", id_paths=prepare_image_list(id), id_next=(id+1), id_prev=(id-1))

@app.route("/camera/")
@app.route("/")
def camera_default(id=0):
    return redirect("/camera/1")

@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'),
                               'favicon.ico', mimetype='image/vnd.microsoft.icon')


generate_flag_png(flag)
app.run(host="0.0.0.0",
        port=1337,
        debug=DEBUG_VAR)