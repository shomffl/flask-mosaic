import cv2
import glob


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
