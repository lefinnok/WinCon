# -*- coding: utf-8 -*-
"""
Created on Wed Sep 16 06:50:10 2020

@author: lefin
"""
import cv2
import math


threshs = [13, 26, 38, 51, 64, 76, 89, 102, 115, 128, 140, 153, 166, 178, 191, 204, 217, 230, 242, 255]
shade = [',', '.', '"', '~', '!', '+', ':', 'v', 'c', 'I', 'o', 'w', '0', 'X', 'P', '$', '#', 'R', 'B', '@']

def renImgPath(path, resY, resX = 0, freeForm = False):
    resY, resX = math.ceil(resY*10/3), math.ceil(resX*10/3)
    img = cv2.imread(path)
    # Do stuff with img
    if img is None:
        return []
    
    height, width, channels = img.shape
    
    #print(height, width)
    
    if freeForm == False:
        img = cv2.resize(img, (resY,round(height*(resY/width)/2)))
    else:
        img = cv2.resize(img, (resY,resX))
    
    #print(height, width)
    
    gimg = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    
    res = []
    
    for row in gimg:
        nrow = []
        for px in row:
            for lvl, thresh in enumerate(threshs):
                if px <= thresh:
                    nrow.append(shade[lvl])
                    break
        res.append(nrow)
    
    return res
