import cv2
import glob
import numpy as np




#フォルダー内の画像の画素値を取得する。
class GetRgb:

    def __init__(self, foldername):
        self.foldername = foldername


    #指定されたフォルダ内の画像の画素値を取得し、一枚のタイルの画素値の平均をリストに格納する。
    def get_rgb(self):
        count_file_num = len(glob.glob(f"./static/images/{self.foldername}/*.png"))
        rgb_list = [cv2.imread(f"./static/images/{self.foldername}/canvas{i}.png").mean(0).mean(0)
                         for i in range(count_file_num)]



        return rgb_list



#オリジナル画像と要素画像の画素値を比較し、最も近い色の要素タイルを選んでいく。
class CompareColors():

    def __init__(self, original, material):
        self.original = original
        self.material = material


    def compare(self):

        original_num = len(self.original)
        material_num = len(self.material)
        difference_list = []
        for j in range(original_num):
            one_tile_difference_list = [((self.original[j][0] - self.material[i][0])**2)+((self.original[j][1] - self.material[i][1])**2)+\
                  ((self.original[j][2] - self.material[i][2])**2) for i in range(material_num)]

            num = min(one_tile_difference_list)
            num2 = one_tile_difference_list.index(num)
            difference_list.append(num2)

        return difference_list


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
