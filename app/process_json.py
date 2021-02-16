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

def retrieve_content(list_slides):
    """
    Retrieves titles and plain texts from slide elements (can get them with breakdown_json)
    Parameters:
        - list_slides : list of data in json format
    """
    keywords = ['level_', 'title_', 'subtitle', 'header']
    doc_content = []
    sublist = []
    filling = False
    for content in list_slides:
        r = [content for keyword in keywords if keyword in content]
        if len(r)==0:
            if content == 'plain_text':
                doc_content.append(sublist)
                sublist = []
                filling = True
            elif filling == True:
                sublist.append(content)
        elif len(r)>0:
            filling = False
    if len(sublist) != 0:
        doc_content.append(sublist)
        
    return doc_content[1:]