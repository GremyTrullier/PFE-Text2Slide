import os
import json

from process_json import *
from slide_functions import *
from pptx import Presentation


def nlp2pptx(json_path):
    pres = Presentation()

    with open(json_path) as f_json:
        data = json.load(f_json)

    pres_name = json_path.rstrip(".json") + ".pptx"
    json_slides = data['document_content']
    slide_elements = []
    breakdown_json(json_slides, slide_elements)
    slide_contents = build_slide_content(slide_elements)
    detect_layout_and_create_slide(slide_contents, pres, json_path.rsplit("/")[0])
    pres.save(pres_name)
    os.startfile(pres_name)