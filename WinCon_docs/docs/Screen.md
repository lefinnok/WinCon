# Screen

This class is a structure class for constructing `Screen` Objects

`Screen` objects are the main object this library uses for managing and displying `Float` objects, 
which are objects that is in similar sort as Widgets in other graphical designing libraries/languages.

##Attributes

|  | base | cursor | setScreen | fps | functions | arguments | columns | rows | fullscreen | scrollSensitivity |
|-:|:----:|:------:|:---------:|:---:|:---------:|:---------:|:-------:|:----:|:----------:|:-----------------:|
|TYPE| list | list | bool | int | list | list | int | int | bool | int |
|DEFAULT| None | None | True | 24 | [] | [] | 0 | 0 | True | 1 |

###base | `list` | `graphical array`
This attribute is default to none, and will generate an empty graphics array as the base graphics if set to None

###cursor | `list` | `graphical array`
This attribute determines the default graphical array for the cursor

###setScreen | `bool`
This attribute determines wether the screen object is to be set to the optimal default state of operation, 
including setting the `column` and `rows` attributes, going fullscreen if `fullscreen == True`, and altering 
the console mode to disable selection mode. 

|#note|  this also disables the keyboard interrupt option

###fps | `int`
This attribute determines the framerate of the screen object, this is crucial for `animated floats` and general timing.

This attribute can also be interpreted as the maximum framerate, or framerate of operation. If the hardware does not allow this framerate,
the `Screen` object will still operate in this particular framerate, but the display may not match this maximum framerate, and therefore some frames 
might be skipped.  

###functions | `list`



###columns | `int`
This attribute determines the number of `columns` the `Screen` has

DEFAULT - `setScreen == True`

this attribute has been set to a set amount due to the scrolling speed of the windows console

###rows | `int`
This attribute determines the number of `rows` the `Screen` has

DEFAULT - `setScreen == True`

this attribute has been set to a set amount due to the scrolling speed of the windows console

