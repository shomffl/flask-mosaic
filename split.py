import cv2
import os



#オリジナル画像を指定したサイズで分割する。
class SplitOriginal:

    def __init__(self, size, filename, filepath):
        self.size = size
        self.filename = filename
        self.filepath = filepath



    def split_image(self):
        img = cv2.imread(self.filename)
        side = img.shape[0]
        img_num = int(side / self.size)

        #座標を指定してオリジナルの画像を切り分けていく。
        original_list = [img[(i * self.size) : ((i+1)*self.size), (j * self.size) : ((j+1) * self.size)]
                         for i in range(img_num) for j in range(img_num)]

        for num, list_num in enumerate(original_list):
            cv2.imwrite(os.path.join("{}/canvas{}.png".format(self.filepath,num)),list_num)
