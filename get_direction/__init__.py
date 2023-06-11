#coding:utf8
"""
how it works:
    1. After typing import sys, enter the path where the package file is located.
    ex) import sys, sys.path.append("/home/usr")
    2. Load class from package folder
    3. Initialize the class
    4. Enter object, direction, angle values.
    5. Execute the set_info() function

manual:
    This api is an api that outputs the name, position, and type of other objects 
    in the range in the form of a dictionary by entering the standard object and the desired direction and angle.
"""
from get_direction import DirectionObjects
