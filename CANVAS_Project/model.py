from .filter_models.artists import *
from .filter_models.normal_filters import *

class StyleTransfer():
    def __init__(self, filter:str, filterType:int, non_filtering_area=None):
        self.filterClassDict={
            "gogh":Gogh,
            "kimhongdo":Kimhongdo,
            "oil_paint":Oil_paint,
            "cartoon":Cartoon,
            
            "k_means":K_means,
            "in":InstanceNorm,
            "black_and_white": Black_And_White,
            "bit" : Bit,
            "custom":"classname"
        }
        self.non_filtering_area = non_filtering_area
        self.modelChoose = self.filterClassDict[filter]
        self.filterModel = self.modelChoose(name = filter, filterType =  filterType)
    
    def coverResult(self, img, res, nfa):
        res = np.array(res)
        img = np.transpose(img,(0,1,2))
        img = cv2.resize(img, (res.shape[1],res.shape[0]))
        w = img.shape[1]
        h = img.shape[0]
        nfa_x1 = int(w*(nfa[0][0]/500))
        nfa_x2 = int(w*(nfa[1][0]/500))
        nfa_y1 = int(h*(nfa[0][1]/500))
        nfa_y2 = int(h*(nfa[1][1]/500))

        x = [nfa_x1, nfa_x2]
        y = [nfa_y1, nfa_y2]

        res[min(y):max(y), min(x):max(x), :] = img[min(y):max(y), min(x):max(x), :]
        return res

    def forward(self, image):
        result = self.filterModel.forward(image)
        result = self.coverResult(image, result, self.non_filtering_area)
        return result