#!/usr/bin/env python
# coding: utf-8
import os
import json
import fileinput

from process_json import *
from nlp_extraction import _run_article_summary

# THIS WILL BE CHANGED TO BE ADAPTED TO THE SCRIPT
datapath = '../data/'
filename = "The Lego Group.json"
jsonpath = datapath+filename

def json2nlp(filename):
    """
    Function that takes a json file as input and summarizes its plain_text content.
    Parameters:
        - filename: json file path that will be modified (a backup is also created)
    Right now there is only one function that summarizes but you can easily change with your own.
    """
    with open(filename) as fjson:
        data = json.load(fjson)

    # we don't care about the beginning of the file
    json_slides = data['document_content']

    # getting the slide elements
    slide_elements = []
    breakdown_json(json_slides, slide_elements)

    # here we will put the best nlp function (14/02 _run_article_summary)
    # just change with your function (str as input and nlp str as output)
    nlp_sentences = {}
    for item in retrieve_content(slide_elements): # get only the plain_text from the slide elements
        nlp_sentences[item[0]] = _run_article_summary(item[0]) # perform nlp on the plain_text

    # write nlp sentences into the file
    # creates a backup file just in case
    for in_sentence, out_sentence in nlp_sentences.items():
        with fileinput.FileInput(nlpjsonpath, inplace = True, backup ='.bak', mode="r") as nlpfile:
            for line in nlpfile:
                if in_sentence in line:
                    print(line.replace(in_sentence, out_sentence), end ='')
                else:
                    print(line, end ='')