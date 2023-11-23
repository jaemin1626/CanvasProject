from .. import utilMethod
import torch
from .filterOption import filterOptions
from ..vgg import get_model
class Artist():
    def __init__(self, 
                num_epochs=300, 
                lr=0.01, 
                content_weight=1e1, 
                style_weight=1e4):

        self.opt = filterOptions(num_epochs=num_epochs, lr=lr, content_weight=content_weight, style_weight=style_weight)

    def draw(self, name, content_tensor, style_tensor):
        device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        con_tensor, sty_tensor = content_tensor, style_tensor
        if name in self.opt.fix_color_imgs:
            con_tensor = utilMethod.change_content_rgb(con_tensor, sty_tensor)
        else:
            sty_tensor = utilMethod.change_style_rgb(con_tensor, sty_tensor)

        con_tensor = utilMethod.transformer(con_tensor).unsqueeze(0).to(device)
        sty_tensor = utilMethod.transformer(sty_tensor).unsqueeze(0).to(device)

        model_vgg = get_model(filter_size=3).features.to(device).eval()
        for param in model_vgg.parameters():
            param.requires_grad_(False)   

        feature_layers = {'0': 'conv1_1',
                        '5': 'conv2_1',
                        '10': 'conv3_1',
                        '19': 'conv4_1',
                        '21': 'conv4_2',  
                        '28': 'conv5_1'}

        content_features = utilMethod.get_features(con_tensor, model_vgg, feature_layers)
        style_features = utilMethod.get_features(sty_tensor, model_vgg, feature_layers)



        input_tensor = con_tensor.clone().requires_grad_(True)
        optimizer = self.opt.optimizer([input_tensor], lr=self.opt.lr)
        content_layer = "conv5_1"
        style_layers_dict = { 'conv1_1': 0.75,
                            'conv2_1': 0.5,
                            'conv3_1': 0.25,
                            'conv4_1': 0.25,
                            'conv5_1': 0.25}

        for epoch in range(self.opt.num_epochs+1):
            if epoch%5 == 0 :
                s = "progress : "+str(100*epoch/self.opt.num_epochs).split('.')[0]+'%'
                print(s,end='')
                print('\r',end='')
            optimizer.zero_grad()
            input_features = utilMethod.get_features(input_tensor, model_vgg, feature_layers)
            content_loss = utilMethod.get_content_loss (input_features, content_features, content_layer)
            style_loss = utilMethod.get_style_loss(input_features, style_features, style_layers_dict)
            neural_loss = self.opt.content_weight * content_loss + self.opt.style_weight * style_loss
            neural_loss.backward(retain_graph=True)
            optimizer.step()

        return utilMethod.imgtensor2pil(input_tensor[0].cpu())
