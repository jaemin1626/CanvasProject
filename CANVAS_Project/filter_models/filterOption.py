from torch import optim
class filterOptions():
    def __init__(self, num_epochs, lr, content_weight, style_weight):
        self.optimizer = optim.Adam
        self.num_epochs = num_epochs
        self.lr = lr
        self.content_weight = content_weight
        self.style_weight = style_weight
        self.paintPath={
            "gogh":{1:"./CANVAS_Project/data/style/gogh/Gogh1.jpg", 2:"./CANVAS_Project/data/style/gogh/Gogh2.jpg",3:"./CANVAS_Project/data/style/gogh//Gogh3.jpg",4:"./CANVAS_Project/data/style/gogh//Gogh4.jpg"},
            "oil_paint":{1:"./CANVAS_Project/data/style/oil_paint/Oil_paint1.jpg", 2:"./data/style/oil_paint/Oil_paint2.jpg", 3:"./data/style/oil_paint/Oil_paint3.jpg", 4:"./data/style/oil_paint/Oil_paint4.jpg", 5:"./data/style/oil_paint/Oil_paint5.jpg"},
            "kimhongdo":{1:"./CANVAS_Project/data/style/kimhongdo/Kimhongdo1.jpg"},
            "cartoon":{1:"./CANVAS_Project/data/style/cartoon/Cartoon1.jpg"}
        }
        self.fix_color_imgs = ["gogh","kimhongdo"]