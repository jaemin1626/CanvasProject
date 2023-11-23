import cv2
from .artistModel import Artist

class Gogh(Artist):
    def __init__(self, name:str, filterType:int):
        super().__init__(num_epochs=60, content_weight=-100000, style_weight=1e4)
        self.name = name
        style_img = cv2.imread(self.opt.paintPath[self.name][filterType])
        self.style_img = cv2.cvtColor(style_img,cv2.COLOR_BGR2RGB)

    def forward(self, content_img):
        res = self.draw(self.name, content_img, self.style_img)
        return res

class Oil_paint(Artist):
    def __init__(self, name:str, filterType:int):
        super().__init__(num_epochs=50, content_weight=1e1, style_weight=1e4)
        self.name = name
        style_img = cv2.imread(self.opt.paintPath[self.name][filterType])
        self.style_img = cv2.cvtColor(style_img,cv2.COLOR_BGR2RGB)

    def forward(self, content_img):
        res = self.draw(self.name, content_img, self.style_img)
        return res

class Kimhongdo(Artist):
    def __init__(self, name:str, filterType:int):
        super().__init__(num_epochs=100, content_weight=1e0, style_weight=1e4)
        self.name = name
        style_img = cv2.imread(self.opt.paintPath[self.name][filterType])
        self.style_img = cv2.cvtColor(style_img,cv2.COLOR_BGR2RGB)

    def forward(self, content_img):
        res = self.draw(self.name, content_img, self.style_img)
        return res

class Cartoon(Artist):
    def __init__(self, name:str, filterType:int):
        super().__init__(num_epochs=300, content_weight=1e0, style_weight=1e4)
        self.name = name
        style_img = cv2.imread(self.opt.paintPath[self.name][filterType])
        self.style_img = cv2.cvtColor(style_img,cv2.COLOR_BGR2RGB)

    def forward(self, content_img):
        res = self.draw(self.name, content_img, self.style_img)
        return res