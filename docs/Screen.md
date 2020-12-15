# Screen

This class is a structure class for constructing `Screen` Objects

`Screen` objects are the main object this library uses for managing and displying `Float` objects, 
which are objects that is in similar sort as Widgets in other graphical designing libraries/languages.

This class also contains the `keyboard listener` and determines the function for keyboard inputs.

##--Arguments--

|  | base | cursor | setScreen | fps | functions | arguments | columns | rows | fullscreen | scrollSensitivity |
|-:|:----:|:------:|:---------:|:---:|:---------:|:---------:|:-------:|:----:|:----------:|:-----------------:|
|TYPE| list | list | bool | int | list | list | int | int | bool | int |
|DEFAULT| None | None | True | 24 | [] | [] | 0 | 0 | True | 1 |

###base | `list` | `graphical array`
This argument is default to none, and will generate an empty graphics array as the base graphics if set to None

###cursor | `list` | `graphical array`
This argument determines the default graphical array for the cursor

###setScreen | `bool`
This argument determines wether the screen object is to be set to the optimal default state of operation, 
including setting the `column` and `rows` arguments, going fullscreen if `fullscreen == True`, and altering 
the console mode to disable selection mode. 

|#note|  this also disables the keyboard interrupt option

###fps | `int`
This argument determines the framerate of the screen object, this is crucial for `animated floats` and general timing.

This argument can also be interpreted as the maximum framerate, or framerate of operation. If the hardware does not allow this framerate,
the `Screen` object will still operate in this particular framerate, but the display may not match this maximum framerate, and therefore some frames 
might be skipped.  

###functions | `list`
This argument contains a list of functions that is to be executed in the `loopFunctions()` function.

###arguments | `list`
This argument contains a list of arguments that is to be put into in the functions within the `functions` argument.

The length of this argument must match the length of the `functions` argument, if no arguments is to be passed into the 
coorisponding function, include an empty list.

###columns | `int`
This argument determines the number of `columns` the `Screen` has

DEFAULT - `setScreen == True`

this argument has been set to a set amount due to the scrolling speed of the windows console

###rows | `int`
This argument determines the number of `rows` the `Screen` has

DEFAULT - `setScreen == True`

this argument has been set to a set amount due to the scrolling speed of the windows console

###fullscreen | `bool`
This argument determines whether the console window will automatically go fullscreen, it is recommended that during testing 
this argument are to be set `False`, or else it will exit the already full screen window, due to the code executed simply 
presses the f11 key using the keyboard module.

###scrollSensitivity | `int`
This argument determines the sensitivity of scrolling within the `Screen` object

used in passing into the `self.cursor` attribute when creating the `Cursor` object

##--Attributes--

###self.functions
attribute of the `functions` argument

###self.arguments
attribute of the `arguments` argument

###self.floats
This attribute is the list containing all the `Float` items within the `Screen` object, this attribute is used in the `render()` 
function where it loops through this list and replace characters one by one according to the placement of `Float` item within the list.

###self.fps
attribute of the `fps` argument

it is used in the `start()` function to calculate the sleep time for each loop.

###self.windim
this attribute stores the pixel count of the current system as a list
where index 0 is the number of pixels in the x axis(columns) and index 1 is the 
number of pixels in the y axis(rows)

###self.col
number of columns of the `Screen` object

###self.row
number of rows of the `Screen` object

###self.base
attribute of the `base` argument

###self.map
the `fMap` object of `Float` objects within the current `Screen` object, it is used for the `Cursor` object

###self.cursor
the `Cursor` object of the current `Screen` object, which itself is a subclass of the `Float` object, 
In most circumstances, it will be put as the first object (index 0) in the `self.floats` list attribute

###self.Ex
the attribute for exiting the `start()` function, False at default

###self.inputTarget
this attribute stores the `Float` object that recieves keyboard inputs

###self.klistener
this attribute is created in the function `kbSetup()`

this attribute stores the keyboard listener of the current `Screen`


##--Functions--
### setFloats | floats: `list`
This function sets the passed list of `floats` as attribute `self.floats`

### addFloats | floats: `list`
This function appends the passed list of `floats` at the end of list attribute `self.floats`

### setBase | base: `list` `graphical array`
This funciton sets the passed list of `base` as the attribute `self.base`

### getBase
returns a deepcopy of attribute `self.base`

### getFloatBC| x:`int`, y:`int`
This functions returns the `Float` object at the given coordinates

### kbSetup
This function sets up the keyboard listener, it is called at the start of the function `start()`

### singleFrameRender
this returns a rendered string of the current frame

### loopFunctions
this executes the functions in attribute `self.functions` with arguments in attribute `self.arguments`

### start
this function starts the display of the current `Screen` object by printing in a loop.

##Usage
	screen = Screen(fps = 60, fullscreen=False, scrollSensitivity=2)

This creates a `Screen` object screen with 60 fps, does not automatically Fullscreens, and with a scrollSensitivity of 2
