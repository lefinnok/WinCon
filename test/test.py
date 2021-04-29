# -*- coding: utf-8 -*-
"""
Created on Thu Dec 24 13:50:08 2020

@author: lefin
"""

from wincon.WinCon import Screen, ImgFloat, GifAnimFloat, Float, AnimFloat,box
import os
import cursor
from timeit import timeit



cursor.hide()

dirname = os.path.dirname(__file__)
filename = os.path.join(dirname, 'relative/path/to/file/you/want')

s = Screen(fps=24, fullscreen=False)
'''
img = GifAnimFloat('pixelart_P4a_438x450.gif', 50,0,0,True,loop=True, fps = 30)

img.start()
'''
img = ImgFloat('GrassTile.png', 5, 9, 0, 0, True)

#f = Float(img.ary[1],101,0,True)

s.addFloats([img])

s.start()

'''
def ren():
    print(s.singleFrameRender())

print(timeit(ren, number=10000))'''