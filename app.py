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


@app.route("/simple", methods=["GET", "POST"])
def simple():
    return render_template("makemosaic.html")


@app.route("/fullscale", methods=["GET", "POST"])
def fullscale():
    return render_template("sendmaterial.html")


@app.route("/sendmaterial", methods=["GET", "POST"])
def sendmaterial():
    shutil.rmtree("./static/images/fullscale_images/big_material_files/")
    shutil.rmtree("./static/images/fullscale_images/download_material_files/")
    shutil.rmtree("./static/images/fullscale_images/small_material_files/")
    os.makedirs("./static/images/fullscale_images/big_material_files/")
    os.makedirs("./static/images/fullscale_images/download_material_files/")
    os.makedirs("./static/images/fullscale_images/small_material_files/")
    if request.method == "POST":
        data = request.files.getlist("file")
        for id,name in enumerate(data):
            ascii_filename = Kakashi.japanese_to_ascii(name.filename)
            save_filename = secure_filename(ascii_filename)
            name.save(os.path.join("./static/images/fullscale_images/download_material_files/", save_filename))

            img = cv2.imread(f"./static/images/fullscale_images/download_material_files/{save_filename}")
            height = img.shape[0]
            width = img.shape[1]
            adjust_height = (41 / height)
            adjust_width = (41/ width)
            img1 = cv2.resize(img, (int(width * adjust_width), int(height * adjust_height)))
            img2 = img1[0: 40, 0: 40]
            cv2.imwrite(f"./static/images/fullscale_images/big_material_files/canvas{id}.png", img2)
            img3 = cv2.resize(img2, (5, 5))
            cv2.imwrite(f"./static/images/fullscale_images/small_material_files/canvas{id}.png", img3)

    return render_template("makemosaic2.html")



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

        SplitOriginal(10, "./static/images/upload_image_files/resize_image.png","./static/images/split_image_files/").split_image()
        read_original = GetRgb("split_image_files")
        read_material = GetRgb("simple_images/small_material_files")
        cul = CompareColors(read_original.get_rgb(), read_material.get_rgb()).compare()
        create = ConnectImage(10, 400, cul,"simple_images")
        create.connect_image()


        return render_template("result.html", result=Markup(result), filepath="./static/images/download_original_files/mosaic_image.png")


@app.route("/result2", methods=["GET", "POST"])
def result2():
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

        SplitOriginal(10, "./static/images/upload_image_files/resize_image.png","./static/images/split_image_files/").split_image()
        read_original = GetRgb("split_image_files")
        read_material = GetRgb("fullscale_images/small_material_files")
        cul = CompareColors(read_original.get_rgb(), read_material.get_rgb()).compare()
        create = ConnectImage(10, 400, cul,"fullscale_images")
        create.connect_image()


        return render_template("result.html", result=Markup(result), filepath="./static/images/download_original_files/mosaic_image.png")




if __name__ == "__main__":
    app.run(debug=True)
