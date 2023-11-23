from numpy import argmax
import numpy as np
import torch
from PIL import Image
from torchvision.transforms.functional import to_pil_image
import torch.nn.functional as F
import torchvision.transforms as transforms

transImgSize = 98304
lrImgSize = 98304
mean_rgb = (0.485, 0.456, 0.406)
std_rgb = (0.229, 0.224, 0.225)

def imgtensor2pil(img_tensor):
    img_tensor_c = img_tensor.clone().detach()
    img_tensor_c*=torch.tensor(std_rgb).view(3, 1, 1)
    img_tensor_c+=torch.tensor(mean_rgb).view(3, 1, 1)
    img_tensor_c = img_tensor_c.clamp(0,1)
    img_pil=to_pil_image(img_tensor_c)
    return img_pil

def get_features(x, model, layers):
    features = {}
    for name, layer in enumerate(model.children()):
        x = layer(x)
        if str(name) in layers:
            features[layers[str(name)]] = x
    return features

def gram_matrix(x):
    n, c, h, w = x.size()
    x = x.view(n*c, h * w)
    gram = torch.mm(x, x.t())
    return gram

def get_content_loss(pred_features, target_features, layer):
    target= target_features[layer]
    pred = pred_features [layer]
    loss = F.mse_loss(pred, target)
    return loss

def get_style_loss(pred_features, target_features, style_layers_dict):  
    loss = 0
    for layer in style_layers_dict:
        pred_fea = pred_features[layer]
        pred_gram = gram_matrix(pred_fea)
        n, c, h, w = pred_fea.shape
        target_gram = gram_matrix (target_features[layer])
        layer_loss = style_layers_dict[layer] *  F.mse_loss(pred_gram, target_gram)
        loss += layer_loss/ (n* c * h * w)
    return loss

def transformer(img):
    ratio = img.shape[1]/img.shape[0]
    tis = transImgSize
    height = (int)((tis/ratio)**(1/2))
    width = (int)(ratio*height)
    transformer = transforms.Compose([
                transforms.Resize((height, width)),  
                transforms.ToTensor(),
                transforms.Normalize(mean_rgb, std_rgb)]) 
    img = Image.fromarray(img) 
    res = transformer(img) 
    return res 

def change_content_rgb(content_tensor, style_tensor):
    c = [content_tensor[:,:,0], content_tensor[:,:,1], content_tensor[:,:,2]]
    s = [style_tensor[:,:,0], style_tensor[:,:,1], style_tensor[:,:,2]]

    cm = [np.mean(i) for i in c ]
    sm = [np.mean(i) for i in s ]

    rm = [se/ce for se,ce in zip(sm,cm)]

    img = np.zeros_like(content_tensor)
    def ceiling(pixel):
        if pixel>255:
            return 255
        else : 
            return pixel
    ceiling = np.vectorize(ceiling)
    for i in range(3):
        img[:,:,i] = ceiling(c[i]*rm[i])
    return img


def change_style_rgb(content_tensor, style_tensor):
    c = [content_tensor[:,:,0], content_tensor[:,:,1], content_tensor[:,:,2]]
    s = [style_tensor[:,:,0], style_tensor[:,:,1], style_tensor[:,:,2]]

    cm = [i.sum() for i in c ]
    sm = [i.sum() for i in s ]

    c_order_index = []
    for _ in range(3):
        index = argmax(cm)
        cm[index] = 0
        c_order_index.append(index)

    s_order_index = []
    for _ in range(3):
        index = argmax(sm)
        sm[index] = 0
        s_order_index.append(index)

    img = np.zeros_like(style_tensor)

    for c_index,s_index in zip(c_order_index,s_order_index):
        img[:,:,c_index] = s[s_index]
    
    return img
