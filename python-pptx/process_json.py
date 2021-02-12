import os
import json

from enum import Enum
from pptx.util import Inches
from pptx import Presentation
from pptx.enum.shapes import MSO_SHAPE

def breakdown_json(list_slides, l):
    """
    Function that read a json file and recursively break down its elements to return them in a list
    Parameters:
        - list_slides : list of data in json format
        - l : the list to be returned
    """
    if (type(list_slides) == type(list())):
        for value in list_slides:
            if type(value) == type(str()):
                l.append(value)
            else:
                breakdown_json(value, l)
    elif (type(list_slides) == type(dict())):
        for key,value in list_slides.items():
            if type(value) == type(str()):
                l.append(value)
            else:
                breakdown_json(value, l)
    else:
        print(type(list_slides))
        

def build_slide_content(slide_elements):
    """
    Function that build the different slide contents using the slide elements
    Parameters:
        - slide_elements : list of all the elements of the slides (can get them using breakdown_json)
    """
    slide_contents = []
    sub_list = []
    for element in slide_elements:
        if(element.split('_')[0] == 'level'):
            slide_contents.append(sub_list)
            sub_list = []
        sub_list.append(element)
        
    slide_contents.append(sub_list)
        
    return slide_contents[1:]