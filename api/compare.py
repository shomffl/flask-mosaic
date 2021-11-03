
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
