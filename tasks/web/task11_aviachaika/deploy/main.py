from pathlib import Path
from flask import Flask, render_template, request
import os
from lxml import etree

app = Flask(
    "task11_reservation",
    template_folder=Path(__file__).parent,
    static_folder=Path(__file__).parent / "static",
)
app.config["UPLOAD_FOLDER"] = "uploads"

# Создание папки для загрузок
if not os.path.exists(app.config["UPLOAD_FOLDER"]):
    os.makedirs(app.config["UPLOAD_FOLDER"])

flag = (
    r"CTF{EXAMPLE}" if "FLAG" not in os.environ else os.environ["FLAG"].replace('"', "")
)
with open("/etc/flag.txt", "w") as f:
    f.write(flag)


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        if "file" not in request.files:
            return "No file part"

        file = request.files["file"]
        if file.filename == "":
            return "No selected file"

        if file and file.filename.endswith(".xml"):
            filepath = os.path.join(app.config["UPLOAD_FOLDER"], file.filename)
            file.save(filepath)

            try:
                parser = etree.XMLParser(resolve_entities=True)
                tree = etree.parse(filepath, parser)
                root = tree.getroot()

                # Допустим, мы хотим получить информацию о бронировании
                booking_info = {
                    "Отель": root.findtext("Отель"),
                    "Дата": root.findtext("Дата"),
                    "Город": root.findtext("Город"),
                }

                return f"Бронирование: {booking_info}"

            except Exception as e:
                return f"Ошибка обработки файла: {str(e)}"

    return render_template("index.html")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=1337)
