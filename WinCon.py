# -*- coding: utf-8 -*-
"""
Created on Mon Sep 14 05:19:28 2020

@author: lefin
"""


from WinConFMod import modRes
from WinConMax import maxCon
from WinConImg import renImgPath
from WinConVid import camVid, finish
from copy import deepcopy
from threading import Thread, active_count
from multiprocessing import Process
import sys
import time
from pynput.keyboard import Key, Controller
from pynput import mouse, keyboard
from win32api import GetSystemMetrics
import ctypes
import math
from math import cos,sin,tan,radians
from pyfiglet import Figlet

transparent = '઻'
#clampT = lambda n,x: min(max(0, n), x)
#clampT = lambda n,x: min(x, max(0, n))
clampT = lambda n,x: min(max(0, x), max(0, n))
clampM = lambda n,x: min(0,max(x,n))
clampZ = lambda n: max(0, n)

#Font Size Setup
def ConSetup(fontSize: int) -> (int, int):
    """
    This function is used for setting up the console to be used as a screen
    It first sets the font size of a windows console
    and it maximize the console

    Parameters
    ----------
    fontSize : int
        The desired font's height (the amount of pixel in the y axis).

    Returns
    -------
    columns : int
        returns the maximum column(x) of the console screen.
        
    rows : int
        returns the maximum row(y) of the console screen.

    """
    rs = fontSize#input('Enter A Font Size: ')
    modRes(rs)
    columns, rows = maxCon()
    return columns,rows


def box(x: int ,y: int, options = [], Title = '', tAlign = 'center', xIntersects = [], yIntersects = []) -> list:
    """
    A function that returns a box

    Parameters
    ----------
    x : int
        the x dimention of box 
        
        note: (to get a square the x dimention will have to be 2y, due to the console font dimention being 1:2)
    
    y : int
        the y dimention of box
    
    options : list, optional
        a list where you can input options to modify the resulting box. The default is [].
        
        t - transparent filling ('઻')
        
        rc - round corners
        
        db - double borders
        
        dc - double corners
        
        hvb - heavy borders
        
        hvc - heavy corners
        
        diag - diagonal corners(doesn't look that good in my opinion')
        
        
        input your options as a list of strings, the options are prioritized
        from the bottom to the top
        
        e.g. ['t','rc']
        with these options, the function will return a box with tranparent fillings
        and round corners.
        
        e.g. ['rc','hvc']
        with these options, the function will return a box with heavy corners, due to
        the heavy corners option being more prioritized(just cause, for no perticular reason)
        note: the order of the options does not affect the priority, the priorities are
        predetermined.

    Returns
    -------
    box
       a array representing a box which fits the ary value of a Float object 

    """
    corners = ['┌','┐','└','┘']
    borders = ['│','─']
    space = ' '
    intersects = ['┬','┴','├','┤','┼']
    ['╧','╤','╟','╢','┼']
    if 't' in options:
        space = '઻'
    if 'rc' in options:
        corners = ['╭','╮','╰', '╯']
    if 'db' in options:
        borders = ['║','═']
    if 'dc' in options:
        corners = ['╔','╗','╚','╝']
    if 'dint' in options:
        intersects = ['╦','╩','╠','╣','╬']
    if 'hvb' in options:
        borders = ['┃','━']
    if 'hvc' in options:
        corners = ['┏','┓','┗','┛']
    if 'diag' in options:
        corners = ['╱','╲','╲','╱']
    
    clampZ = lambda n: max(0, n)
    top = [corners[0][:],corners[1][:]]
    bottom = [corners[2][:],corners[3][:]]
    mid = [borders[0][:],borders[0][:]]
    xinter = [intersects[2][:],intersects[3][:]]
    yinter = [intersects[0][:], intersects[1][:]]
    for _ in range(clampZ(x-1)-1):
        top.insert(1,borders[1][:])
        bottom.insert(1,borders[1][:])
        mid.insert(1,space)
        xinter.insert(1,borders[1][:])
    box = [top[:],bottom[:]]
    for _ in range(clampZ(y-1)-1):
        yinter.insert(1,borders[0][:])
        box.insert(1,mid[:])
    
    
    if Title != '':
        title = list(Title)
        if tAlign == 'center':
            startingIndex = center(len(box[0]), len(title))
        if tAlign == 'left':
            startingIndex = 1
        if tAlign == 'right':
            startingIndex = len(box[0]) - len(title) - 1
        for cidx, char in enumerate(title):
            box[0][(startingIndex+cidx)%len(box[0])] = char
            
    for yin in yIntersects:
        box[yin] = xinter[:]
    
    for xin in xIntersects:
        for pxid, px in enumerate(yinter[:]):
            if box[pxid][xin] is borders[1] and pxid != 0 and pxid != len(yinter)-1:
                box[pxid][xin] = intersects[4]
                continue
            box[pxid][xin] = px
    
    return box




def empty(col: int,row: int) -> list:#returns an empty screen
    """
    This function is used to generate an empty 2d list(array) to be acted as
    the base of a screen, the size of which is determined by the
    column and row attributes

    Parameters
    ----------
    col : int
        the number of columns of the screen.
        
    row : int
        the number of rows of the screen.

    Returns
    -------
    emptyScreen: list
        the empty screen array.

    """
    emptyScreen = []
    emptyLine = []
    for space in range(col):
        emptyLine.append(' ')
    for space in range(row):
        emptyScreen.append(emptyLine.copy())
    
    return emptyScreen

def render(screen) -> str:#returns a rendered sting of the screen combining the floats and base
    """
    This function is used to render a screen object and returns a printable string
    the floats/windows/widgets/objects/whatever is rendered on top of the base dependeing on their coordinates and order
    each character is then joined on each line as a line string
    and each line is then joined to form the screen string

    Parameters
    ----------
    screen : Screen Object
        The screen object which is wished to be rendered.

    Returns
    -------
    scr : str
        the printable screen string.

    """
    scr = deepcopy(screen.base)
    for floa in screen.floats[:]: #loop through each float
        if floa.enable == False:
            continue
        x = floa.x
        y = floa.y
        '''fyc = (y + len(floa.ary)/2)*0
        fxc = (x + len(floa.ary[0])/2)*0
        theta = floa.rotation'''
        for lidx, line in enumerate(floa.get()): #loop through each line
            for pxidx, px in enumerate(line): #loop through each pixel/character
                if px == '઻':
                    continue
                '''if floa.rotation != 0:
                    fx = round(cos(radians(theta))*((x + pxidx) - fxc) + sin(radians(theta))*((y + lidx) - fyc))
                    fy = round(-sin(radians(theta))*((x + pxidx) - fxc) + cos(radians(theta))*((y + lidx) - fyc))
                    scr[fy%screen.row][fx%screen.col] = px
                    continue'''
                scr[(y + lidx)%screen.row][(x + pxidx)%screen.col] = px #for each pixel/char of the float object, the pixels/chars of the base screen at the displaced x y coordinate of the float object will be replaced by the pixel/char of the float object 
                #print(y + lidx, x + pxidx)
            
    #pack screen to string
    for idx,line in enumerate(scr):
        scr[idx] = ''.join(line)
    
    scr.pop(-1)
    scr = ''.join(scr)
    return scr

def textReplace(aryMain, ary: list, increment, padding = (0,0,0,0), vertical = True):
    res = deepcopy(aryMain)
    if vertical:
        for lidx, line in enumerate(ary[increment:]): #loop through each line
            if lidx >= (len(res) - padding[1] - 1):
                break
            for pxidx, px in enumerate(line): #loop through each pixel/character
                res[lidx + padding[0]][(pxidx + padding[2])%(len(aryMain[0]) - padding[3])] = px #for each pixel/char of the float object, the pixels/chars of the base screen at the displaced x y coordinate of the float object will be replaced by the pixel/char of the float object 
    else:
        for lidx, line in enumerate(ary): #loop through each line
            if lidx >= (len(res) - padding[1] - 1):
                break
            for pxidx, px in enumerate(line[increment:]): #loop through each pixel/character
                if pxidx >= (len(res[0]) - padding[3] - 1):
                    break
                res[lidx + padding[0]][(pxidx + padding[2])%(len(aryMain[0]) - padding[3])] = px #for each pixel/char of the float object, the pixels/chars of the base screen at the displaced x y coordinate of the float object will be replaced by the pixel/char of the float object 
    return res

def replace(floaMain, ary: list, x: int, y: int, padding = (0,0,0,0)):
    """
    The function adds the ary to the float object, similar to the render function,
    but permanent and with a single ary instead of float objects.

    Parameters
    ----------
    floaMain : TYPE
        The float.
    ary : list
        The graphic ary.
    x : int
        relative x coordinate.
    y : int
        relative y coordinate.
    padding : Iterable, optional
        Padding(top,bottom,left,right). The default is (0,0,0,0).

    Returns
    -------
    None.

    """
    for lidx, line in enumerate(ary): #loop through each line
        for pxidx, px in enumerate(line): #loop through each pixel/character
            if px == '઻':
                continue
            floaMain.ary[(y + lidx + padding[0])%(floaMain.row - padding[1])][(x + pxidx + padding[2])%(floaMain.col - padding[3])] = px #for each pixel/char of the float object, the pixels/chars of the base screen at the displaced x y coordinate of the float object will be replaced by the pixel/char of the float object 

def center(main, sub):
    """
    This function returns the neccesary coordinate to center the sub object

    Parameters
    ----------
    main : int
        main object dimention on the same axis.
    sub : int
        sub object dimention on the same axis.

    Returns
    -------
    coor
        the coordinate on the axis of the main and sub if the sub is to be centered.

    """
    return int(main/2) - int(sub/2)
    

def fixRateCount(fps: int,frame: list,loop: bool,frameNum: int):
    """
    a fix rate count function for animated float objects

    Parameters
    ----------
    fps : int
        DESCRIPTION.
    frame : list
        DESCRIPTION.
    loop : bool
        DESCRIPTION.
    frameNum : int
        DESCRIPTION.

    Returns
    -------
    None.

    """
    sec = 1/fps
    clampZ = lambda n: max(0, n)
    btime = time.time()
    if loop:
        while 1:
            time.sleep(clampZ(sec-(time.time()-btime)))
            frame[0] = (frame[0] + 1)%frameNum
            btime = time.time()
    else:
        for _ in range(frameNum-1):
            time.sleep(clampZ(sec-(time.time()-btime)))
            frame[0] += 1
            btime = time.time()


        

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
    def __init__(self, ary, x, y, enable, invisible = False, screenCol = 226):
        self.ary = ary
        self.x = x
        if self.x == 'center':
            self.x = center(screenCol,max([len(line) for line in ary]))
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
    
    def targets(self, x = 0, y = 0):
        return self
    
        
        

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
        self.textAry = txtAry
        self.f = flex
        self.irow = self.row
        self.icol = self.col
        self.flex = len(self.textAry) - len(self.ary) + padding[0] + padding[1] + self.f
   
    def get(self):
        self.increment = clampT(self.increment, self.flex)
        
        self.ary[(-self.padding[0])-1][(-self.padding[3])-1] = '▼'
        if self.increment >= self.flex:
            self.ary[(-self.padding[0])-1][(-self.padding[3])-1] = ' '
        if self.increment == 0:
            self.ary[(self.padding[1])][(-self.padding[3])-1] = ' '
        else:
            self.ary[(self.padding[1])][(-self.padding[3])-1] = '▲'
        return textReplace(self.ary, self.textAry, self.increment, padding = self.padding)
    
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
        self.flex = len(self.textAry) - len(self.ary) + self.padding[0] + self.padding[1] + self.f
    
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
        self.flex = len(self.textAry) - len(self.ary) + self.padding[0] + self.padding[1] + self.f
    
    def fResize(self):
        self.icol = self.col
        self.irow = self.row


class InputBox(Float):
    def aryUpdate(self):
        txtAry = []
        for line in self.text:
            words = ''.join(line).split(' ')
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
            txtAry.append([])
        self.textAry = txtAry
        self.flex = len(self.textAry) - len(self.ary) + self.padding[0] + self.padding[1] + self.f
        '''
        self.pointerCoordinate = [len(self.textAry[-2]) - 1 + self.pointerDisplace[0],len(self.textAry) - 2 + self.pointerDisplace[1]]
        
        if self.input == True:
            self.textAry[self.pointerCoordinate[1]].insert(self.pointerCoordinate[0],self.pointer)
        '''
    
    def __init__(self, sx, sy, x, y, enable, padding = (1,1,1,1), increment = 0, flex = 0, invisible = False, noticeText = 'Input here:', keepNoticeText = False, text = [[]], Title = '', tAlign = 'left'):
        self.sx = sx
        self.sy = sy
        self.tAlign = tAlign
        self.flex = flex
        self.Title = Title
        ary = box(sx,sy,Title = self.Title,tAlign = self.tAlign)
        super().__init__(ary, x, y, enable, invisible)
        self.padding = padding
        self.increment = increment
        self.noticeText = noticeText
        self.keepNoticeText = keepNoticeText
        if text != [[]]:
            self.text = text
        else:
            self.text = [list(noticeText)]
        self.input = False
        self.f = flex
        '''
        self.pointer = '|'
        self.pointerDisplace = [0,0]
        self.pointerCoordinate = [0,0]
        '''
        self.aryUpdate()
        
        
        
    def startInput(self):
        self.input = True
        self.ary = box(self.sx,self.sy,options=['dc','db'],Title = self.Title,tAlign = self.tAlign)
        if not self.keepNoticeText and self.text == [list(self.noticeText)]:
            self.text = [[]]
        self.aryUpdate()
        
    def Input(self, char):
        if len(repr(char)) > 3:
            return
        self.text[-1].append(char)
        self.aryUpdate()
        self.increment = self.flex
        
    def specialFunc(self, key):
        if key is Key.backspace:
            if self.text != [[]]:
                if self.text[-1] == []:
                    self.text.pop()
                else:
                    self.text[-1].pop()
            self.aryUpdate()
        
        if key is Key.space:
            self.text[-1].append(' ')
            self.aryUpdate()
            
        if key is Key.enter:
            self.text.append([])
            self.aryUpdate()
        self.increment = self.flex
        
    
    def stopInput(self):
        self.input = False
        self.ary = box(self.sx,self.sy,Title = self.Title,tAlign = self.tAlign)
        if self.text == [[]]:
            self.text = [list(self.noticeText)]
        self.aryUpdate()
    
    def get(self):
        self.increment = clampT(self.increment, self.flex)
        
        self.ary[(-self.padding[0])-1][(-self.padding[3])-1] = '▼'
        if self.increment >= self.flex:
            self.ary[(-self.padding[0])-1][(-self.padding[3])-1] = ' '
        if self.increment == 0:
            self.ary[(self.padding[1])][(-self.padding[3])-1] = ' '
        else:
            self.ary[(self.padding[1])][(-self.padding[3])-1] = '▲'
            
        return textReplace(self.ary, self.textAry, self.increment, padding = self.padding)

    def getText(self):
        return self.text


class InputField(Float):
    def aryUpdate(self):
        self.flex = len(self.text[0]) - len(self.ary[0]) + self.padding[0] + self.padding[1] + self.f
        '''
        self.pointerCoordinate = [len(self.textAry[-2]) - 1 + self.pointerDisplace[0],len(self.textAry) - 2 + self.pointerDisplace[1]]
        
        if self.input == True:
            self.textAry[self.pointerCoordinate[1]].insert(self.pointerCoordinate[0],self.pointer)
        '''
    
    def __init__(self, sx, x, y, enable, padding = (1,1,1,1), increment = 0, flex = 0, invisible = False, noticeText = 'Input here:', keepNoticeText = False, text = [[]], Title = '', tAlign = 'left'):
        self.sx = sx
        self.sy = 3
        self.flex = flex
        self.Title = Title
        self.tAlign = tAlign
        ary = box(self.sx,self.sy,Title = self.Title,tAlign = self.tAlign)
        super().__init__(ary, x, y, enable, invisible)
        self.padding = padding
        self.increment = increment
        self.noticeText = noticeText
        self.keepNoticeText = keepNoticeText
        if text != [[]]:
            self.text = text
        else:
            self.text = [list(noticeText)]
        self.input = False
        self.f = flex
        '''
        self.pointer = '|'
        self.pointerDisplace = [0,0]
        self.pointerCoordinate = [0,0]
        '''
        self.aryUpdate()
        
        
        
    def startInput(self):
        self.input = True
        self.ary = box(self.sx,self.sy,options=['dc','db'],Title = self.Title,tAlign = self.tAlign)
        if not self.keepNoticeText and self.text == [list(self.noticeText)]:
            self.text = [[]]
        self.aryUpdate()
        
    def Input(self, char):
        if len(repr(char)) > 3:
            return
        self.text[0].append(char)
        self.aryUpdate()
        self.increment = self.flex
        
    def specialFunc(self, key):
        if key is Key.backspace:
            if self.text != [[]]:
                self.text[0].pop()
            self.aryUpdate()
        
        if key is Key.space:
            self.text[0].append(' ')
            self.aryUpdate()
            
        if key is Key.enter:
            self.text.append([])
            self.aryUpdate()
        self.increment = self.flex
        
    
    def stopInput(self):
        self.input = False
        self.ary = box(self.sx,self.sy,Title = self.Title,tAlign = self.tAlign)
        if self.text == [[]]:
            self.text = [list(self.noticeText)]
        self.aryUpdate()
    
    def get(self):
        self.increment = clampT(self.increment, self.flex)
        return textReplace(self.ary, self.text, self.increment, padding = self.padding, vertical = False)

    def getText(self):
        return self.text



class AnimFloat(Float): #object class for animated floats
    def start(self):
        
        def counter():
            self.playing = True
            sec = 1/self.fps
            clampZ = lambda n: max(0, n)
            btime = time.time()
            if self.loop:
                while 1:
                    time.sleep(clampZ(sec-(time.time()-btime)))
                    self.frame = (self.frame + 1)%len(self.arys)
                    btime = time.time()
            else:
                for _ in range(len(self.arys)-1):
                    time.sleep(clampZ(sec-(time.time()-btime)))
                    self.frame += 1
                    btime = time.time()
            self.playing = False
        
        if not self.playing:
            self.thread = Thread(target = counter)
            self.thread.daemon = True
            self.thread.start()

    def __init__ (self, arys: list, x: int, y: int, enable: bool, fps = 24, loop = False, invisible = False, playOnStart = False):
        super().__init__(arys, x, y, enable, invisible)
        self.arys = arys
        self.loop = loop
        self.fps = fps
        self.frame = 0
        self.playing = False
        if playOnStart:
            self.start()
        
    def get(self):
        return self.arys[self.frame]
    
    



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
    def __init__(self,text,sx,sy,x,y,enable,functions = [], arguments = [],invisible=False):
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
        self.boxArg[2] = ['rc']
        self.ary = box(*self.boxArg)
        replace(self,[list(self.text)],center(self.col,len(self.text)),center(self.row,1))
    
    def onHover(self):
        self.boxArg[2] = ['rc','hvb']
        self.ary = box(*self.boxArg)
        replace(self,[list(self.text)],center(self.col,len(self.text)),center(self.row,1))
    
    def onHoverLeave(self):
        self.boxArg[2] = ['rc']
        self.ary = box(*self.boxArg)
        replace(self,[list(self.text)],center(self.col,len(self.text)),center(self.row,1))




class Label(Float):
    def __init__(self, text, x, y, enable, invisible = False):
        if type(text) is str:
            ary = [list(text)]
        else:
            ary = [list(str(text))]
        super().__init__(ary, x, y, enable, invisible)

class FigletLabel(Float):
    def __init__(self, text, font, x, y, enable, invisible = False, screenCol = 226,justify = 'auto', width = 226):
        figlet = Figlet(font=font,justify = justify)
        figlet.width = width
        text = figlet.renderText(text)
        text = text.split('\n')
        ary = [list(line) for line in text]
        super().__init__(ary, x, y, enable, invisible,screenCol)


class Frame(Float):
    def getMax(self):
        if len(self.floats) == 0:
            return
        mCol = []
        mRow = []
        for floa in self.floats:
            mCol.append(floa.col + floa.x)
            mRow.append(floa.row + floa.y)
        self.max = [clampZ(max(mRow) - self.row) + 2 + self.flex[1],clampZ(max(mCol)-self.col)+2 + self.flex[0]]
        
    def __init__(self, floats, sx, sy, x, y, enable, screen, dx = 0, dy = 0, options = [], invisible = False, padding = (1,1,1,1), flex = (1,1), drag = 5, vertical = True, horizontal = True, Title = ''):
        ary = box(sx,sy,options,Title,'left')
        super().__init__(ary, x, y, enable, invisible)
        self.floats = floats
        self.padding = padding
        self.dx = dx
        self.dy = dy
        self.idx = self.dx
        self.idy = self.dy
        self.move = False
        self.mx = 0
        self.my = 0
        self.flex = flex
        self.max = []
        self.getMax()
        self.drag = drag
        self.screen = screen
        self.rV = [0,0]
        self.threads = []
        self.vertical = vertical
        self.horizontal = horizontal
        
    def get(self):
        scr = deepcopy(self.ary)
        for floa in self.floats[:]: #loop through each float
            if floa.enable == False:
                continue
            x = floa.x + self.dx
            y = floa.y + self.dy
            for lidx, line in enumerate(floa.get()): #loop through each line
                if y + lidx + self.padding[0] >= self.row - self.padding[1]:
                    break
                if y + lidx + self.padding[0] <= 0 - self.padding[1] + 1:
                    continue
                for pxidx, px in enumerate(line): #loop through each pixel/character
                    if x + pxidx + self.padding[2] >= self.col - self.padding[3]:
                        break
                    if px == '઻' or x + pxidx + self.padding[2] <= 0 - self.padding[3]  + 1:
                        continue
                    scr[y + lidx + self.padding[0]][x + pxidx + self.padding[2]] = px #for each pixel/char of the float object, the pixels/chars of the base screen at the displaced x y coordinate of the float object will be replaced by the pixel/char of the float object 
                    #print(y + lidx, x + pxidx)
        return scr
    
    
    
    def smove(self,x,y):
        self.getMax()
        self.move = True
        self.mx = x
        self.my = y
        self.idx = self.dx
        self.idy = self.dy
    
    def moving(self,x,y):
        dx = x - self.mx
        dy = y - self.my
        if self.horizontal:
            self.dx = clampM(self.idx + dx, -self.max[1])
        if self.vertical:
            self.dy = clampM(self.idy + dy, -self.max[0])
        #self.dx = self.idx + dx
        #self.dy = self.idy + dy
        
    def fmove(self, releaseVel = [0,0]):
        self.rV = releaseVel[:]
        def remainVel():
            const = int(28.52534/self.drag)
            if self.drag == 1:
                const += 1
            batime = time.time()
            sec = 2/self.screen.fps
            while int(self.rV[0]) != 0 and int(self.rV[1]) != 0:
                if abs(int(self.rV[0])) == const and abs(int(self.rV[1])) == const:
                    break
                tm = clampZ(sec-(time.time()-batime))
                sdx = self.dx + int(self.rV[0] * tm)
                sdy = self.dy + int(self.rV[1] * tm)
                if  sdx >= -self.max[1] and sdx < 0 and self.horizontal:
                    self.dx = sdx
                if sdy >= -self.max[0] and sdy < 0 and self.vertical:
                    self.dy = sdy
                self.rV[0] -= int(self.drag * tm * self.rV[0])
                self.rV[1] -= int(self.drag * tm * self.rV[1])
                time.sleep(tm)
                batime = time.time()
            self.threads.pop(0)
            sys.exit()
            
        
        velThread = Thread(target = remainVel)
        velThread.daemon = True
        if len(self.threads) < 1:
            self.threads.append(velThread)
            self.threads[0].start()
            
        
            
        self.move = False
            
    
    def targets(self, x, y):
        if self.move:
            return self
        tx = x - self.x - self.padding[2]
        ty = y - self.y - self.padding[0]
        for floa in self.floats:
            if type(floa) in [Button,InputField,InputBox] and not floa.invisible:
                fx = floa.x + self.dx
                fy = floa.y + self.dy
                if tx in range(fx, fx + floa.col) and ty in range(fy, fy + floa.row):
                    return floa.targets()
        return self
        


class Form(Frame):
    def __init__(self, fields, sx, sy, x, y, enable, screen, dx = 0, dy = 0, options = [], invisible = False, padding = (1,1,1,1), flex = (1,1), drag = 5, buttons = ['Submit','Cancel'], functions = [], arguments = [], Title = '' ):
        self.fields = []
        self.buttons = []
        for fidx, field in enumerate(fields):
            self.fields.append(InputField(sx - padding[2] - padding[3] -2, 0, fidx * 3,True,noticeText = '', Title = field))
        for bidx, button in enumerate(buttons):
            self.buttons.append(Button(button,len(button) + 4,3,center(sx,len(button) + 4)-1, len(self.fields) * 3 + bidx * 3, True,functions[bidx],arguments[bidx]))
        super().__init__(self.fields + self.buttons, sx, sy, x, y, enable, screen, dx, dy, options, invisible, padding, flex, drag, horizontal = False,Title=Title)
        
class Menu(Frame):
    def __init__(self, buttons, sx, sy, x, y, enable, screen, dx = 0, dy = 0, options = [], invisible = False, padding = (1,1,1,1), flex = (1,1), drag = 5, functions = [], arguments = [], Title = '' ):
        self.buttons = []
        for bidx, button in enumerate(buttons):
            self.buttons.append(Button(button,len(button) + 4,3,center(sx,len(button) + 4)-1, bidx * 3, True))
        super().__init__(self.buttons, sx, sy, x, y, enable, screen, dx, dy, options, invisible, padding, flex, drag, horizontal = False,Title=Title)   
        
        #super().__init__(floats, sx, sy, x, y, enable, screen, dx, dy, options, invisible, padding, flex, drag, horizontal = False)
    
    




class Cursor(Float):
    def __init__(self,ary,screen,scrollSensitivity = 1):
        super().__init__(ary, 0, 0, True, True)
        self.scrollSensitivity = scrollSensitivity
        self.click = False
        self.x = 0
        self.y = 0
        self.screen = screen
        self.target = None
        self.target_cache = None
        self.velx = 0
        self.vely = 0
        self.recVel = [self.velx, self.vely]
        self.scrollable = [TextBox, InputBox, InputField]
        self.draggable = [Frame, Form]
        
        def on_move(x, y):
            self.x = int(x * self.screen.reldim[0])
            self.y = int(y * self.screen.reldim[1])
            
            
            #drag/move/resize floats
            if hasattr(self.target, 'moving'):
                if hasattr(self.target_cache,'onHoverLeave'):
                    self.target_cache.onHoverLeave()
                    self.target_cache = None
                    
                if self.target.move:
                    self.target.moving(self.x,self.y)
            
            #float targeting
            for mp in self.screen.map.map[::-1]:
                if self.x in mp[0][0] and self.y in mp[0][1]:
                    self.target_cache = self.target
                    self.target = mp[1].targets(self.x,self.y)
                    break
            else:
                if self.target is not None:
                    if type(self.target) is Button:
                        self.target.onHoverLeave()
                    if type(self.target) in self.draggable:
                        self.target.fmove()
                    self.target_cache = self.target
                    self.target = None
            
                
            
        def on_click(x, y, button, pressed):
            self.click = pressed
            if not pressed:
                self.recVel = [self.velx, self.vely]
            else:
                if self.screen.inputTarget is not None and self.target is not self.screen.inputTarget:
                    self.screen.inputTarget.stopInput()
                    self.screen.inputTarget = None
                    
            if hasattr(self.target, 'onClick') and hasattr(self.target, 'onRelease'):
                if pressed:
                    self.target.onClick()
                else:
                    self.target.onRelease()
            if hasattr(self.target,'smove') and hasattr(self.target,'fmove'):
                if pressed:
                    self.target.smove(self.x,self.y)
                else:
                    if self.target.move:
                        self.target.fmove(self.recVel)
            if hasattr(self.target,'startInput'):
                if pressed:
                    self.screen.inputTarget = self.target
                    self.screen.inputTarget.startInput()
        
        def on_scroll(x, y, dx, dy):
            self.scroll = dy * self.scrollSensitivity
            if hasattr(self.target, 'increment'):
                self.target.increment -= self.scroll
            if hasattr(self.target, 'vertical') and hasattr(self.target, 'horizontal') and hasattr(self.target, 'max'):
                if self.target.vertical and not self.target.horizontal:
                    self.target.dy = clampM(self.target.dy + self.scroll, -self.target.max[0])
                if not self.target.vertical and self.target.horizontal:
                    self.target.dx = clampM(self.target.dx + self.scroll, -self.target.max[1])
        
        self.listener = mouse.Listener(on_move=on_move, on_click=on_click, on_scroll=on_scroll)
        self.listener.start()
        
        #cursor velocity
        def calVel():
            batime = time.time()
            sec = 1.5/self.screen.fps
            while 1:
                ux, uy = self.x, self.y
                tm = clampZ(sec-(time.time()-batime))
                time.sleep(tm)
                vx, vy = self.x, self.y
                self.velx, self.vely = ((vx-ux)/tm),((vy-uy)/tm)
                batime = time.time()
                
        self.velThread = Thread(target = calVel)
        self.velThread.daemon = True
        self.velThread.start()
        
                
    
    def start(self):
        def lp():
            batime = time.time()
            sec = 1/self.screen.fps
            while 1:
                time.sleep(clampZ(sec-(time.time()-batime)))
                batime = time.time()
                
                if type(self.target) is Button and self.click is False:
                    self.target.onHover()
        
        self.thread = Thread(target = lp)
        self.thread.daemon = True
        self.thread.start()
                


        

class fMap():
    def __init__(self, floats):
        self.map = []
        for floa in floats:
            if floa.invisible:
                continue
            fx = floa.x
            fy = floa.y
            self.map.append([[list(range(fx, fx + floa.col)),list(range(fy, fy+floa.row))],floa])


class Screen(): #object class for screens
    """
    This class is a structur class for Screen Objects
    
    Attributes
    ----------
    columns : int
        the number of columns(x dimention) the screen object has
        
    rows : int
        the number of rows(y dimention) the screen object has
        
    base : list
        the base image of the screen, could be used with the empty function to create
        a blank screen
    """
    def __init__ (self, base = None, cursor = None, setScreen = True, fps = 24, functions = [], arguments = [], columns = 0, rows = 0, fullscreen = True, path = None, scrollSensitivity = 1):
        self.functions = functions
        self.arguments = arguments
        self.floats = []
        self.fps = fps
        #screen setup
        if setScreen == True:
            self.windim = [GetSystemMetrics(0),GetSystemMetrics(1)]
            
            self.col,self.row = ConSetup(self.windim[1]/64)
            
            if fullscreen:
                self.keyboard = Controller()
                self.keyboard.press(Key.f11)
                self.keyboard.release(Key.f11)
            
            self.col,self.row = ConSetup(self.windim[1]/64)
            self.fontSize = self.windim[1]/64
            self.reldim = [self.col/self.windim[0],self.row/self.windim[1]] #the windows and screen resolution ratio
            
            
            kernel32 = ctypes.windll.kernel32
            kernel32.SetConsoleMode(kernel32.GetStdHandle(-10), 128)
        else:
            self.col = columns
            self.row = rows
        
        #base setup
        if base == None:
            base = empty(self.col,self.row)
        self.base = base
        
        #cursor setup
        self.map = fMap(self.floats)
        if cursor == None:
            self.cursor = Cursor([['╳','઻'],['઻','╲']],self,scrollSensitivity)
        self.cursor.start()
        
        #other setup
        self.floats.append(self.cursor)
        
        self.Ex = False
        
        self.posL = []
        
        self.inputTarget = None
        

    
    def setFloats(self, floats):
        self.floats = floats
        self.floats.append(self.cursor)
        self.map = fMap(self.floats)
    
    def addFloats(self, floats):
        self.floats.remove(self.cursor)
        self.floats += floats
        self.floats.append(self.cursor)
        self.map = fMap(self.floats)
    
    def setBase(self, base):
        self.base = base
        
    def getBase(self):
        ast = self.base.copy()
        return ast
    
    def getFloatBC(self, x, y): #get float items by coordinate
        for floa in self.floats[::-1]:
            if (type(floa) is AnimFloat) or floa.invisible == True:
                continue
            fx = floa.x
            fy = floa.y
            if (x in range(fx, fx + floa.col)) and (y in range(fy, fy+floa.row)):
                return floa.targets()
        return None
    
    def kbSetup(self):
        def on_press(key):
            if self.inputTarget is not None:
                if hasattr(key,'char'):
                    #alphbetical numeric keys
                    self.inputTarget.Input(key.char)
                else:
                    #functional keys
                    self.inputTarget.specialFunc(key)
            
        def on_release(key):
            if key == keyboard.Key.esc:
                self.Ex = True
            
        self.klistener = keyboard.Listener(on_press=on_press, on_release=on_release)
        self.klistener.start()
    
    def singleFrameRender(self):
        return render(self)
    
    def loopFunctions(self):
        for function,arguments in zip(self.functions,self.arguments):
            function(*arguments)
    
    def start(self):
        self.kbSetup()
        batime = time.time()
        sec = 1/self.fps
        while 1:
            if self.Ex == True:
                sys.exit()
            time.sleep(clampZ(sec-(time.time()-batime)))
            batime = time.time()
            print(render(self),end='\r')
            
            '''
            #testing codes
            self.loopFunctions()
            self.floats[-2] = Label('{},{},{}'.format(self.cursor.x,self.cursor.y,self.cursor.target), 0, 0, True)
            '''
            







'''
#Testing Code
fpss = 60#int(input('fps: '))
    
screenX = Screen(fps = fpss, fullscreen=False, scrollSensitivity=2)


asg = list('@@BBRR##$$PPXX00wwooIIccvv::++!!~~""..,,')

asgs = Float([asg,asg,asg,asg,asg,asg,asg,asg,asg,asg,asg,asg,asg,asg],50,20,True)
asgsm = Float(renImgPath(r'C:\PythonScripts\PythonWinCon\image\tst.jpg',80),100,0,True)
asgsm = ImgFloat(r'C:\PythonScripts\PythonWinCon\image\tst.jpg', 0, 10, 100, 0, True)

asgsa = ImgFloat(r'C:\PythonScripts\PythonWinCon\image\tst.jpg', 0, 70, 10, 10, True)
btn2 = Button('EFGH',8,3,0,0,True)
btn3 = Button('EFGH',16,5,100,100,True)

frm = Frame([asgsa,btn2,btn3],100,50,100,0,True,screenX,drag = 2, horizontal = False)
#flt = Float(box(10,5,['hvb','dc']),40,40,True, invisible=True)

lorem = 'Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.'


a = []

def xa(x):
    x.append(1)

btn = Button('ABCD',8,11,20,40,True,[xa],[[a]])
    

tb = TextBox(50, 10, 5, 5, True, lorem, flex=3)

ibx = InputBox(50,10,56,5,True, Title = 'Ibx',tAlign = 'center')
ipf = InputField(50,56,16,True)

aft = AnimFloat([[['-','>']], [['-','-','>']],[['-','-','-','>']], [['-','-','-','-','>']]], 3, 3, True, loop=False, fps=2)

lb = Label(a, 0, 0, True)

#frrm = Form(['First Name', 'Last Name', 'Blah', 'Blah Blah'], 31, 10, 56, 19, True, screenX,Title = 'Name Form')

bxtst = Float(box(20,10,xIntersects = [6,4,8], yIntersects = [2,4,6]),10,10,True)
#asgs.rotation = 95

screenX.addFloats([asgs,asgsm,tb,btn,aft,frm,ibx,ipf,bxtst,lb])

aft.start()
aft.start()
aft.start()

screenX.start()





sys.exit()
'''