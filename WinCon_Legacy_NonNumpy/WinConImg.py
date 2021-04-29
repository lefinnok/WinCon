# -*- coding: utf-8 -*-
"""
Created on Wed Sep 16 06:50:10 2020

@author: lefin
"""

import math
from PIL import Image

threshs = [13, 26, 38, 51, 64, 76, 89, 102, 115, 128, 140, 153, 166, 178, 191, 204, 217, 230, 242, 255]
shade = [',', '.', '"', '~', '!', '+', ':', 'v', 'c', 'I', 'o', 'w', '0', 'X', 'P', '$', '#', 'R', 'B', '@']

def renImgPath(path, resY, resX = 0, freeForm = False):
    #resY, resX = math.ceil(resY*10/3), math.ceil(resX*10/3)
    img = Image.open(path)
    # Do stuff with img
    if img is None:
        return [[]]
    
    width,height = img.size
    
    #print(height, width)
    
    if freeForm == False:
        img = img.resize((resY,round(height*(resY/width)/2)))
    else:
        img = img.resize((resY,resX))
    
    #print(height, width)
    gimg = img.convert('LA')
    width,height = gimg.size
    
    gimg = list(gimg.getdata())
    gimg = [gimg[x*width:(x+1)*width] for x in range(height)]
    res = []
    
    for row in gimg:
        nrow = []
        for px in row:
            for lvl, thresh in enumerate(threshs):
                if px[0] <= thresh:
                    nrow.append(shade[lvl])
                    break
        res.append(nrow)
    
    return res

#print(renImgPath('C:/PythonScripts/WinCon_Git/test/8832079fe99eb68cbc3d59312abfb76f.jpg',10))
def change_contrast(img, level):
    factor = (259 * (level + 255)) / (255 * (259 - level))
    def contrast(c):
        return 128 + factor * (c - 128)
    return img.point(contrast)




def renGif2Anim(path, resY, resX = 0, freeForm = False, contrast = 0):
    imgs = Image.open(path)
    if imgs is None or not imgs.is_animated:
        return [[]]
    numFrame = imgs.n_frames
    frames = []
    for f in range(numFrame):
        imgs.seek(f)
        frames.append(imgs.copy())
    
    fres = []
    for img in frames:
        img = change_contrast(img, contrast)
        width,height = img.size
        
        #print(height, width)
        
        if freeForm == False:
            img = img.resize((resY,round(height*(resY/width)/2)))
        else:
            img = img.resize((resY,resX))
        
        #print(height, width)
        gimg = img.convert('LA')
        width,height = gimg.size
        
        gimg = list(gimg.getdata())
        gimg = [gimg[x*width:(x+1)*width] for x in range(height)]
        res = []
        
        for row in gimg:
            nrow = []
            for px in row:
                for lvl, thresh in enumerate(threshs):
                    if px[0] <= thresh:
                        nrow.append(shade[lvl])
                        break
            res.append(nrow)
        fres.append(res)
    return fres
#print(len(renGif2Anim('C:/PythonScripts/WinCon_Git/test/tenor.gif',10)))