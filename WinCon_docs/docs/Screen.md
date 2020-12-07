# Screen

This class is a structure class for constructing `Screen` Objects

`Screen` objects are the main object this library uses for managing and displying `Float` objects, 
which are objects that is in similar sort as Widgets in other graphical designing libraries/languages.

##Attributes

|  | base | cursor | setScreen | fps | functions | arguments | columns | rows | fullscreen | scrollSensitivity |
|-:|:----:|:------:|:---------:|:---:|:---------:|:---------:|:-------:|:----:|:----------:|:-----------------:|
|TYPE| list | list | bool | int | list | list | int | int | bool | int |
|DEFAULT| None | None | True | 24 | [] | [] | 0 | 0 | True | 1 |

###base
This attribute is default to none, and will generate an empty graphics array as the base graphics if set to None

###cursor
This attribute determines the default graphical array for the cursor

###setScreen
This attribute determines wether the screen object is to be set to the optimal default state of operation, 
including setting the 

###columns
This attribute determines the number of `columns` the `Screen` has

DEFAULT

this attribute has been set to a set amount due to the scrolling speed of the windows console

###rows
This attribute determines the number of `rows` the `Screen` has

this attribute has been set to a set amount due to the scrolling speed of the windows console

