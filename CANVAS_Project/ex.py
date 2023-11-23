import cv2
import numpy as np
import torch
contentPath= "./data/style/gogh/Gogh1.jpg"
content_img = cv2.imread(contentPath, cv2.IMREAD_COLOR)

b = content_img[:,:,0]
g = content_img[:,:,1]
r = content_img[:,:,2]

rm = np.mean(r)
gm = np.mean(g)
bm = np.mean(b)

img = np.zeros_like(content_img)
z = np.zeros_like(content_img[:,:,0])
for c in [[r,g,b],[r,b,g],[b,g,r],[b,r,g],[g,r,b],[g,b,r]]:
    for i in range(3):
        img[:,:,i] = c[i]
    img[:,:,0]= b
    img[:,:,1]= z
    img[:,:,2]= z
    
cs = torch.tensor(content_img)

def change_rgb(content_tensor, style_tensor):
    c = [content_tensor[:,:,0], content_tensor[:,:,1], content_tensor[:,:,2]]
    s = [style_tensor[:,:,0], style_tensor[:,:,1], style_tensor[:,:,2]]

    cm = [torch.sum(i) for i in c ]
    sm = [torch.sum(i) for i in s ]

change_rgb(cs,cs)
