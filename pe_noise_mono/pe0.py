from math import ceil,floor
from PIL import Image
from random import randrange
import numpy
class RGB:
    def __init__(self,r,g,b):
        self.rgb = (r,g,b)
        try:self.rule = RGB_op_rule
        except: self.rule = lambda x:x%256
    def __add__(self,oth):
        return RGB(self.rule(self.rgb[0]+oth.rgb[0]),self.rule(self.rgb[1]+oth.rgb[1]),self.rule(self.rgb[2]+oth.rgb[2]))
    def __sub__(self,oth):
        return RGB(self.rule(self.rgb[0]-oth.rgb[0]),self.rule(self.rgb[1]-oth.rgb[1]),self.rule(self.rgb[2]-oth.rgb[2]))
    def __mul__(self,oth):
        return RGB(self.rule(self.rgb[0]*oth),self.rule(self.rgb[1]*oth),self.rule(self.rgb[2]*oth))
    def __div__(self,oth):
        return RGB(self.rule(self.rgb[0]/oth),self.rule(self.rgb[1]/oth),self.rule(self.rgb[2]/oth))
    def __mod__(self,oth):
        return RGB(self.rule(self.rgb[0]%oth),self.rule(self.rgb[1]%oth),self.rule(self.rgb[2]%oth))
    def __repr__(self):
        return self.rgb.__repr__()
    def __str__(self):
        return self.rgb.__str__()
        
def dot(f,m,x,y):
    res = m[0][0][0]-m[0][0][0]
    #print(f.h,f.w,f.d)
    for i in range(f.h):
        for j in range(f.w):
            for d in range(f.d):
                try:
                    res += m[d][y+j][x+i] * f[d][i][j]
                except:
                    break
    return res
def dotImg(f,img,x,y):
    res = RGB(0,0,0)
    for i in range(f.w):
        for j in range(f.h):
            try:
                res += RGB(*img.getpixel((x+i,y+j)))*f[0][j][i]
            except:
                break
    return res.rgb
    
class Filter: 
    def __init__(self,w=1,h=1,d=1,**arg):
        self.f = []
        if 'fx' in arg:
            self.fx = arg['fx']
        else:
            self.fx = lambda x,y,z: randrange(256)
        if 'img' in arg:
            img = arg['img'].convert('L')
            self.d = 1
            self.w = img.size[0]
            self.h = img.size[1]
            for i in range(self.h):
                row = []
                for j in range(self.w):
                    row.append(img.getpixel((j,i)))
                self.f.append(row)
            self.f = [self.f]
        else:
            for i in range(d):
                layer = []
                for j in range(h):
                    row = []
                    for k in range(w):
                        row.append(self.fx(i,j,k))
                    layer.append(row)
                self.f.append(layer)
            self.w = w
            self.h = h
            self.d = d
    def __getitem__(self,x):
        return self.f[x]
    def __str__(self):
        return self.f.__str__()
    def __repr__(self):
        return self.f.__repr__()
    def apply(self,mat,dist = 0):
        d = len(mat)
        h = len(mat[0])
        w = len(mat[0][0])
        if self.d!=d:
            raise Exception('deepth error {},{}'.format(self.d,d))
        res = []
        for i in range(0,h,dist if dist else self.h):
            nrow = []
            for j in range(0,w,dist if dist else self.w):
                nrow.append(dot(self,mat,j,i))
            res.append(nrow)
        return [res]
    def applyImg(self,img,dist = 0):
        if self.d!=1:
            raise Exception('deepth error')
        res = Image.new(img.mode,(img.size[0]//dist,img.size[1]//dist) if dist else (img.size[0]//self.w,img.size[1]//self.h))
        print(res.size)
        x,y = 0,0
        for i in range(0,img.size[0],dist if dist else self.w):
            y = 0
            for j in range(0,img.size[1],dist if dist else self.h):
                try:
                    res.putpixel((x,y),dotImg(self,img,i,j))
                except:
                    break
                y+=1
            x+=1
        print(x,y)
        return res
def noise_gate(f):
    return Filter(f.w,f.h,f.d,fx=lambda x,y,z:f.f[x][y][z]+0.2*(x+1)+0.1*y+0.1*z)

def mono_gate(img):
    res = Image.new(img.mode,img.size)
    for i in range(res.size[0]):
        for j in range(res.size[1]):
            p = img.getpixel((i,j))
            if max(p)>255//2:
                p = (min(int(p[0]*1.3),255),min(int(p[1]*1.1),255),min(int(p[2]*1.1),255))
            else:
                p = (floor(p[0]*0.7),floor(p[1]*0.9),floor(p[2]*0.9))
            res.putpixel((i,j),p)
    return res