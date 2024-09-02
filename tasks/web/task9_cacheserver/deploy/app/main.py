#!/usr/bin/env python

from flask import Flask, request, redirect, send_from_directory, send_file, render_template
import os

flag = r'CTF{EXAMPLE}' if 'FLAG' not in os.environ else os.environ['FLAG'].replace('"','')
DEBUG_VAR = True


app = Flask("task9_cacheserver",
            template_folder="./templates",
            static_folder="./static")
         
app.config['UPLOAD_FOLDER'] = "./uploads/"
   
@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'),
                               'favicon.ico', mimetype='image/vnd.microsoft.icon')

@app.route("/")
def index():
    return redirect("/load?file=./")


@app.route("/upload", methods=["GET", "POST"])
def upload_route():
    if request.method == "GET":
        return render_template("upload.html")
    if request.method == "POST":
        f = request.files["file"]
        print(f.filename)
        f.save(os.path.join(app.config['UPLOAD_FOLDER'],f.filename))
        return redirect("/load?file=./")


@app.route("/load")
def load_route():
    base_dir = app.config['UPLOAD_FOLDER']
    inner_dir = request.args.get("file")
    full_dir  = base_dir
    if inner_dir is not None:
        full_dir += inner_dir
    listing = []
    if os.path.exists(full_dir):
        if os.path.isdir(full_dir):
            for f in os.listdir(full_dir):
                if os.path.isdir(f):
                    listing.append("./" + f + "/")
                else:
                    listing.append("./" + f)
                    
        elif os.path.isfile(full_dir):
            return send_file(full_dir,as_attachment=True)
        else:
            return "Error 500", 500

    return render_template("load.html", files=listing)

@app.route("/clear_cache")
def clear_cache():
    # TODO: Rewrite legacy script
    res = os.popen("sh ./clear.sh").read()
    return res, 200

if __name__ == "__main__":
    with app.app_context():
        app.run(host="0.0.0.0",
        port=1337,
        debug=DEBUG_VAR)