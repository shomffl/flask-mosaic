from flask import Flask, request, redirect, url_for, render_template, Markup
from werkzeug.utils import secure_filename
import os
import shutil
import pykakasi
from PIL import Image
from split import SplitOriginal
from get_rgb import GetRgb, CompareColors, ConnectImage
import cv2


class Kakashi:
    kakashi = pykakasi.kakasi()
    kakashi.setMode("H", "a")
    kakashi.setMode("K", "a")
    kakashi.setMode("J", "a")
    conv = kakashi.getConverter()

    @classmethod
    def japanese_to_ascii(cls, japanese):
        return cls.conv.do(japanese)

UPLOAD_FOLDER = "./static/images/"
ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "gif"}

app = Flask(__name__)
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER



def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route("/", methods=["GET", "POST"])
def index():
    return render_template("index.html")


@app.route("/result", methods=["GET", "POST"])
def result():
    if request.method == "POST":
        # ファイルの存在と形式を確認
        if "file" not in request.files:
            print("File doesn't exist!")
            return redirect(url_for("index"))
        file = request.files["file"]
        if not allowed_file(file.filename):
            print(file.filename + ": File not allowed!")
            return redirect(url_for("index"))

        # ファイルの保存
        # shutil.rmtree(UPLOAD_FOLDER)
        # os.mkdir(UPLOAD_FOLDER)
        filename = secure_filename(file.filename)  # ファイル名を安全なものに
        filepath = os.path.join(UPLOAD_FOLDER+"upload_image_files", filename)
        file.save(filepath)

        # 画像の読み込み
        image = Image.open(filepath)
        image = image.convert("RGB")
        image = image.resize((400, 400))
        new_path= os.path.join(UPLOAD_FOLDER+"upload_image_files", "resize_image.png")
        image.save(new_path)

        SplitOriginal(8, "./static/images/upload_image_files/resize_image.png","./static/images/split_image_files/").split_image()
        read_original = GetRgb("split_image_files")
        read_material = GetRgb("simple_images/small_material_files")
        cul = CompareColors(read_original.get_rgb(), read_material.get_rgb()).compare()
        create = ConnectImage(8, 400, cul,"simple_images")
        create.connect_image()


        return render_template("result.html", result=Markup(result), filepath="./static/images/download_original_files/mosaic_image.png")





if __name__ == "__main__":
    app.run(debug=True)
