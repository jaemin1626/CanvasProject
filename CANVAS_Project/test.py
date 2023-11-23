from PIL import Image
import utilMethod
import torch
import matplotlib.pylab as plt
import torchvision.models as models

path2content= "./data/content/con1.jpg"
path2style= "./data/style/oil_paint/Oil_paint2.jpg"
content_img = Image.open(path2content)
style_img = Image.open(path2style)
opt = Option()


content_tensor = opt.transformer(content_img)
style_tensor = opt.transformer(style_img)
input_tensor = content_tensor.clone().requires_grad_(True)

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

model_vgg = models.vgg19(pretrained=True).features.to(device).eval()
for param in model_vgg.parameters():
    param.requires_grad_(False)   

feature_layers = {'0': 'conv1_1',
                  '5': 'conv2_1',
                  '10': 'conv3_1',
                  '19': 'conv4_1',
                  '21': 'conv4_2',  
                  '28': 'conv5_1'}

con_tensor = content_tensor.unsqueeze(0).to(device)
sty_tensor = style_tensor.unsqueeze(0).to(device)

content_features = utilMethod.get_features(con_tensor, model_vgg, feature_layers)
style_features = utilMethod.get_features(sty_tensor, model_vgg, feature_layers)



input_tensor = con_tensor.clone().requires_grad_(True)
optimizer = opt.optimizer([input_tensor], lr=opt.lr)
content_layer = "conv5_1"
style_layers_dict = { 'conv1_1': 0.75,
                      'conv2_1': 0.5,
                      'conv3_1': 0.25,
                      'conv4_1': 0.25,
                      'conv5_1': 0.25}

for epoch in range(opt.num_epochs+1):
    optimizer.zero_grad()
    input_features = utilMethod.get_features(input_tensor, model_vgg, feature_layers)
    content_loss = utilMethod.get_content_loss (input_features, content_features, content_layer)
    style_loss = utilMethod.get_style_loss(input_features, style_features, style_layers_dict)
    neural_loss = opt.content_weight * content_loss + opt.style_weight * style_loss
    neural_loss.backward(retain_graph=True)
    optimizer.step()

plt.imshow(utilMethod.imgtensor2pil(input_tensor[0].cpu()))
plt.show()