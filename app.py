from flask import Flask, request, redirect, url_for, render_template, Markup
from werkzeug.utils import  secure_filename
import os
import shutil
import pykakasi
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


app = Flask(__name__)
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER






@app.route("/", methods=["GET", "POST"])
def index():
    return render_template("index.html")


@app.route("/result", methods=["GET", "POST"])
def result():
    if request.method == "POST":
        file = request.files["file"]

        # ファイルの保存
        filename = secure_filename(file.filename)  # ファイル名を安全なものに
        filepath = os.path.join(UPLOAD_FOLDER+"upload_image_files", filename)
        file.save(filepath)

        shutil.rmtree(f"{UPLOAD_FOLDER}split_images_file")
        os.mkdir(f"{UPLOAD_FOLDER}split_images_file")

        # 画像の読み込み
        image = cv2.imread(filepath)
        height = image.shape[0]
        width = image.shape[1]
        longer_one = max(height, width)
        adjust_per = 400 / longer_one
        adjust_height = int(round(height * adjust_per, -1))
        adjust_width = int(round(width * adjust_per, -1))

        resize_image = cv2.resize(image, dsize=(adjust_width, adjust_height))
        new_path= os.path.join(UPLOAD_FOLDER+"upload_image_files", "resize_image.png")
        cv2.imwrite(new_path, resize_image)

        split = SplitOriginal(5, f"{UPLOAD_FOLDER}upload_image_files/resize_image.png",f"{UPLOAD_FOLDER}split_images_file/")
        length = split.split_image()
        height_num = length[0]
        width_num = length[1]

        read_original = GetRgb("split_images_file")
        read_material = GetRgb("simple_images/small_material_files")
        cul = CompareColors(read_original.get_rgb(), read_material.get_rgb()).compare()
        create = ConnectImage(height_num, width_num, cul,"simple_images")
        create.connect_image()


        return render_template("result.html", height = int(adjust_height * 1.5), width = int(adjust_width * 1.5), filepath="./static/images/download_original_files/mosaic_image.png")





if __name__ == "__main__":
    app.run(debug=True)
