# -*- coding: utf-8 -*-
"""
Created on Thu Sep 24 21:51:30 2020

@author: lefin
"""

class Float(): #object class for floats
    """
    This class is a structure class for Float Objects
    
    Attributes
    ----------
    ary : list
        The ASCII image/2D-list(array) for the float object, 
        first dimention for lines,
        second dimention for characters.
        
    x : int
        The x(column) coordiniate for the float object
        
    y : int
        The y(row) coordinate for the float object
        
    enable : bool
        enable/disable the Float accordingly
    """
    def __init__(self, ary, x, y, enable, invisible = False):
        self.ary = ary
        self.x = x
        self.y = y
        self.enable = enable
        self.invisible = invisible
        self.row = len(self.ary)
        if self.row == 0:
            self.col = 0
        else:
            self.col = len(self.ary[0])
        
    def get(self):
        return self.ary
    
class TextBox(Float):
    def __init__(self, sx, sy, x, y, enable, text, padding = (1,1,1,1), increment = 0, options = [], flex = 0, invisible = False):
        self.options = options
        ary = box(sx,sy,options)
        super().__init__(ary, x, y, enable, invisible)
        self.padding = padding
        self.increment = increment
        self.itext = text
        words = self.itext.split(' ')
        txtAry = []
        ln = []
        val = (self.col - (padding[2] + padding[3]))
        for word in words:
            ws = list(word)
            if len(ws) + len(ln) + 1 < val:
                ln += ws + [' ']
            else:
                txtAry.append(ln[:])
                ln = []
                ln += ws + [' ']
        txtAry.append(ln[:])
        self.text = txtAry
        self.f = flex
        self.irow = self.row
        self.icol = self.col
        self.flex = len(self.text) - len(self.ary) + padding[0] + padding[1] + self.f
   
    def get(self):
        self.increment = clampT(self.increment, self.flex)
        
        self.ary[(-self.padding[0])-1][(-self.padding[3])-1] = '▼'
        if self.increment >= self.flex:
            self.ary[(-self.padding[0])-1][(-self.padding[3])-1] = ' '
        if self.increment == 0:
            self.ary[(self.padding[1])][(-self.padding[3])-1] = ' '
        else:
            self.ary[(self.padding[1])][(-self.padding[3])-1] = '▲'
        return textReplace(self.ary, self.text, self.increment, padding = self.padding)
    
    def setText(self, text):
        words = text.split(' ')
        txtAry = []
        ln = []
        val = (self.col - (self.padding[2] + self.padding[3]))
        for word in words:
            ws = len(word)
            if len(ws) + len(ln) + 1 < val:
                ln += ws + [' ']
            else:
                txtAry.append(ln[:])
                ln = []
                ln += ws + [' ']
        txtAry.append(ln[:])
        self.text = txtAry
        self.flex = len(self.text) - len(self.ary) + self.padding[0] + self.padding[1] + self.f
    
    def resize(self,ux,uy,vx,vy):
        dx = vx-ux
        dy = vy-uy
        sx = self.icol + dx - 1
        sy = self.irow + dy - 1
        self.ary = box(sx,sy,self.options)
        self.row = len(self.ary)
        if self.row == 0:
            self.col = 0
        else:
            self.col = len(self.ary[0])
        words = self.itext.split(' ')
        txtAry = []
        ln = []
        val = (self.col - (self.padding[2] + self.padding[3]))
        for word in words:
            ws = list(word)
            if len(ws) + len(ln) + 1 < val:
                ln += ws + [' ']
            else:
                txtAry.append(ln[:])
                ln = []
                ln += ws + [' ']
        txtAry.append(ln[:])
        self.text = txtAry
        self.flex = len(self.text) - len(self.ary) + self.padding[0] + self.padding[1] + self.f
    
    def fResize(self):
        self.icol = self.col
        self.irow = self.row

class AnimFloat(Float): #object class for animated floats
    def __init__ (self, arys: list, x: int, y: int, enable: bool, fps = 24, loop = False, invisible = False):
        super().__init__(arys, x, y, enable, invisible)
        self.arys = arys
        self.loop = loop
        self.fps = fps
        self.frame = [0]
        self.thread = Thread(target = fixRateCount, args = (self.fps,self.frame,self.loop,len(self.arys)))
        self.thread.daemon = True
        self.thread.start()
    def get(self):
        return self.arys[self.frame[0]]

class ImgFloat(Float):
    def __init__(self, path, sx, sy, x, y, enable, invisible = False, freeForm = False):
        self.path = path
        self.freeForm = freeForm
        ary = renImgPath(path, sy, sx, freeForm)
        super().__init__(ary, x, y, enable, invisible)
        self.irow = self.row
        self.icol = self.col
    def resize(self,ux,uy,vx,vy):
        dx = vx-ux
        dy = vy-uy
        sx = self.icol + dx - 1
        sy = self.irow + dy - 1
        self.ary = renImgPath(self.path, sy, sx, self.freeForm)
        self.row = len(self.ary)
        if self.row == 0:
            self.col = 0
        else:
            self.col = len(self.ary[0])
    def setFF(self, freeForm):
        self.freeForm = freeForm
    
    def fResize(self):
        self.icol = self.col
        self.irow = self.row
        
class Button(Float):
    def __init__(self,text,sx,sy,x,y,enable,invisible=False,functions = [], arguments = []):
        self.functions = functions
        self.arguments = arguments
        self.text = text
        self.boxArg = [sx,sy,['rc']]
        ary = box(*self.boxArg)
        super().__init__(ary, x, y, enable, invisible)
        replace(self,[list(text)],center(self.col,len(text)),center(self.row,1))
        self.click = False
    def onClick(self):
        self.click = True
        
        self.boxArg[2] = ['rc','db']
        self.ary = box(*self.boxArg)
        replace(self,[list(self.text)],center(self.col,len(self.text)),center(self.row,1))
        
        returns = []
        for function,arguments in zip(self.functions,self.arguments):
            Return = function(*arguments)
            returns.append(Return)
        return returns
    def onRelease(self):
        self.click = False
    
    def onHover(self):
        self.boxArg[2] = ['rc','hvb']
        self.ary = box(*self.boxArg)
        replace(self,[list(self.text)],center(self.col,len(self.text)),center(self.row,1))
    
    def onHoverLeave(self):
        self.boxArg[2] = ['rc']
        self.ary = box(*self.boxArg)
        replace(self,[list(self.text)],center(self.col,len(self.text)),center(self.row,1))

class Cursor(Float):
    def __init__(self,ary):
        super().__init__(ary, 0, 0, True, True)
        self.click = False