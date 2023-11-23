import cv2
import numpy as np
class K_means():
    def __init__(self, name:str, filterType:int):
        self.k = 3
        self.epoch = 5
        pass
    
    def resize_img(self, content_img):
        x = content_img.shape[0]
        y = content_img.shape[1]
        a = 512/(x*y)**(1/2)
        new_x = int(a*x)
        new_y = int(a*y)
        return cv2.resize(content_img,(new_y,new_x))

    def make_centroid(self, k, content_img):
        m = 255
        cen = np.random.rand(k,3)
        cen = cen*m
        return cen

    def clustering(self, k,cen,content_img):
        cluster = [[] for _ in range(k)]
        x = content_img.shape[0]
        y = content_img.shape[1]

        for xkey in range(x):
            for ykey in range(y):
                dist = []
                for c in cen:
                    dist.append((c[0]-content_img[xkey][ykey][0])**2+(c[1]-content_img[xkey][ykey][1])**2)
                mindex = np.argmin(dist)
                cluster[mindex].append((xkey,ykey))
        return cluster
    
    def renewalCen(self, cluster, content_img):
        cen = []
        for clus in cluster:
            clen = len(clus)
            if clen == 0 : continue
            bsum, gsum, rsum = 0, 0, 0
            for key in clus:
                bsum += content_img[key[0]][key[1]][0]
                gsum += content_img[key[0]][key[1]][1]
                rsum += content_img[key[0]][key[1]][2]
            bmean, gmean, rmean = bsum/clen, gsum/clen, rsum/clen
            cen.append([bmean, gmean, rmean])
        return cen

    def filtering(self, cen, cluster, content_img):
        img = content_img.copy()
        for i, c in enumerate(cen):
            for index in cluster[i]:
                img[index[0]][index[1]][0] = c[0]
                img[index[0]][index[1]][1] = c[1]
                img[index[0]][index[1]][2] = c[2]
        return img

    def forward(self, content_img):
        content_img = self.resize_img(content_img)
        cen = self.make_centroid(self.k, content_img)
        for e in range(self.epoch):
            if e%1 == 0 :
                s = "progress : "+str(100*e/self.epoch).split('.')[0]+'%'
                print(s,end='')
                print('\r',end='')
            cluster = self.clustering(self.k,cen,content_img)
            cen = self.renewalCen(cluster,content_img)
        res = self.filtering(cen, cluster, content_img)
        
        return res

class InstanceNorm():
    def __init__(self, name:str, filterType:int):
        pass
        
    def filtering(self, content_img):
        img = content_img.copy()
        c = img
        c_mean = np.mean(c)
        cm = c-c_mean
        val = (np.sum(cm*cm)**(1/2))/c.size
        c = cm/val
        c_min = np.min(c)
        c_max = np.max(c)
        c = c/c_max
        c=c*255
        img = c
        return img

    def forward(self, content_img):
        res = self.filtering(content_img)
        return res

class Black_And_White():
    def __init__(self, name:str, filterType:int):
        pass
        
    def filtering(self, content_img):
        img = content_img
        img = np.mean(img,axis=2,dtype=int)
        return img

    def forward(self, content_img):
        res = self.filtering(content_img)
        return res

class Bit():
    def __init__(self, name:str, filterType:int):
        pass
        
    def filtering(self, content_img):
        img = content_img
        h = img.shape[0]
        w = img.shape[1]
        ratio = int((h*w)**(1/2)//50)
        img = cv2.resize(img,(w//ratio,h//ratio))
        img = cv2.resize(img,(w,h),interpolation=cv2.INTER_NEAREST)
        return img

    def forward(self, content_img):
        res = self.filtering(content_img)
        return res