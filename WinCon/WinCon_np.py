# -*- coding: utf-8 -*-
"""
Created on Sat Jan  2 15:15:11 2021

@author: lefin
"""

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
            base = np.zeros(self.col,self.row)
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
            '''
            #testing codes
            #self.loopFunctions()
            self.floats[-1].ary = [list(str(int(1/(time.time()-batime))))] 
            '''
            
            
            batime = time.time()
            print(render(self),end='\r')
            