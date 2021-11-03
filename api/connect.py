import cv2
import numpy as np

#画像を結合する
class ConnectImage():

    def __init__(self, height_num, width_num, min_numbers, course_name):
        self.height_num = height_num
        self.width_num = width_num
        self.min_numbers = min_numbers
        self.course_name = course_name

    def connect_image(self):
        list1 = np.array_split(self.min_numbers, self.height_num)
        big_img = []
        for i in list1:
            small_img = []
            for j in range(self.width_num):
                read = cv2.imread(f"./static/images/{self.course_name}/big_material_files/canvas{i[j]}.png")
                small_img.append(read)
            big_img.append(small_img)


        cul = cv2.vconcat([cv2.hconcat(i) for i in big_img])


        cv2.imwrite("./static/images/download_original_files/mosaic_image.png", cul)
