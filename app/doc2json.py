import json
import mammoth
from bs4 import BeautifulSoup

STYLE_MAP = """
p[style-name='Title'] => h4:fresh
p[style-name='Heading 1'] => h1:fresh
p[style-name='Heading 2'] => h2:fresh
p[style-name='Heading 3'] => h3:fresh
p[style-name^='Heading'] => h3:fresh
p[style-name='List'] => ui:fresh
p[style-name='i'] => strong
p[style-name='b'] => em
"""


def doc2json(file_path):
    file_name = file_path.rstrip('.docx')
    json_path = file_name + ".json"
    b = open(file_name + '.html', 'wb')
    with open(file_path, "rb") as docx_file:
        document = mammoth.convert_to_html(docx_file, style_map=STYLE_MAP)
    b.write(document.value.encode('utf8'))
    docx_file.close()
    b.close()

    soup = BeautifulSoup(document.value + "\n", "html.parser")

    i = 0
    level = -1
    level_text = [-1]
    content = ''
    end = ['']
    while soup.contents[i] != "\n":  # lecture du fichier html
        if soup.contents[i].name == "h4":  # si title
            level = 0
            content += '{' + '"type":"level_0","content":[{"type":"title_0","content":["' + soup.contents[
                i].text.replace('"', "'") + '"]}'
            if soup.contents[i].next.next.name != "p":
                content += ','

        if soup.contents[i].name == "h1":  # si h1
            level = 1
            if level_text[-1] == 1:
                content += end[-1]
                content += '{' + '"type":"level_1","content":[{"type":"title_1","content":["' + soup.contents[
                    i].text.replace('"', "'") + '"]}'
            if level_text[-1] < 1:
                level_text += [1]
                content += '{' + '"type":"level_1","content":[{"type":"title_1","content":["' + soup.contents[
                    i].text.replace('"', "'") + '"]}'
                temp = ']},' + "\n"
                end += [temp]
            if level_text[-1] > 1:
                while level_text[-1] > 1:
                    content += end[-1][:-2]
                    end = end[:-1]
                    level_text = level_text[:-1]
                if level_text[-1] != 1:
                    level_text += [1]
                    content += '{' + '"type":"level_1","content":[{"type":"title_1","content":["' + soup.contents[
                        i].text.replace('"', "'") + '"]}'
                    temp = ']},' + "\n"
                    end += [temp]
                else:
                    content += end[-1]
                    content += '{' + '"type":"level_1","content":[{"type":"title_1","content":["' + soup.contents[
                        i].text.replace('"', "'") + '"]}'

        if soup.contents[i].name == "h2":  # si h2
            level = 2
            if level_text[-1] == 2:
                content += end[-1]
                content += '{' + '"type":"level_2","content":[{"type":"title_2","content":["' + soup.contents[
                    i].text.replace('"', "'") + '"]}'
            if level_text[-1] < 2:
                level_text += [2]
                content += ',{' + '"type":"level_2","content":[{"type":"title_2","content":["' + soup.contents[
                    i].text.replace('"', "'") + '"]}'
                temp = ']},' + "\n"
                end += [temp]
            if level_text[-1] > 2:
                while level_text[-1] > 2:
                    content += end[-1][:-2]
                    end = end[:-1]
                    level_text = level_text[:-1]
                if level_text[-1] != 2:
                    level_text += [2]
                    content += '{' + '"type":"level_2","content":[{"type":"title_2","content":["' + soup.contents[
                        i].text.replace('"', "'") + '"]}'
                    temp = ']},' + "\n"
                    end += [temp]
                else:
                    content += end[-1]
                    content += '{' + '"type":"level_2","content":[{"type":"title_2","content":["' + soup.contents[
                        i].text.replace('"', "'") + '"]}'

        if soup.contents[i].name == "h3":  # si h3
            level = 3
            if level_text[-1] == 3:
                content += end[-1]
                content += '{' + '"type":"level_3","content":[{"type":"title_3","content":["' + soup.contents[
                    i].text.replace('"', "'") + '"]}'
            if level_text[-1] < 3:
                level_text += [3]
                content += ',{' + '"type":"level_3","content":[{"type":"title_3","content":["' + soup.contents[
                    i].text.replace('"', "'") + '"]}'
                temp = ']},' + "\n"
                end += [temp]
            if level_text[-1] > 3:
                while level_text[-1] > 3:
                    content += end[-1][:-2]
                    end = end[:-1]
                    level_text = level_text[:-1]
                if level_text[-1] != 3:
                    level_text += [3]
                    content += '{' + '"type":"level_3","content":[{"type":"title_3","content":["' + soup.contents[
                        i].text.replace('"', "'") + '"]}'
                    temp = ']},' + "\n"
                    end += [temp]
                else:
                    content += end[-1]
                    content += '{' + '"type":"level_3","content":[{"type":"title_3","content":["' + soup.contents[
                        i].text.replace('"', "'") + '"]}'

        if soup.contents[i].name == "ul":  # si liste
            content += ',{"type":"plain_text","content":['
            for l in soup.contents[i]:
                content += '"' + l.text.replace('"', "'") + '",'
            content = content[:-1]
            content += ']}]}' + "\n"

        if (soup.contents[i].name != "h4" and soup.contents[i].name != "h1" and soup.contents[i].name != "h2" and
                soup.contents[i].name != "h3" and soup.contents[i].name != "ul"):  # si autre
            if level == 0:
                content += ',{"type":"plain_text","content":["' + soup.contents[i].text.replace('"',
                                                                                                "'") + '"]}]},' + "\n"
            else:
                content += ',{"type":"plain_text","content":["' + soup.contents[i].text.replace('"', "'") + '"]}' + "\n"

        i += 1  # incrémentation de balise
    while len(end) != 1:
        content += end[-1][:-2]
        end = end[:-1]

    d = open(json_path, 'w')
    # if(json_path == "test.json"):
    #    d.write('{"document_name":"'+json_path+'","document_content":['+"\n"+content)
    # elif(json_path == "The Lego Group.json"):
    #    d.write('{"document_name":"'+json_path+'","document_content":['+"\n"+content+']}]}')
    # elif(json_path == "Walt Disney.json"):
    #    d.write('{"document_name":"'+json_path+'","document_content":['+"\n"+content)
    d.write(
        '{"document_name":"' + json_path + '","document_content":[' + "\n" + content + ']}]}]}]}]}]}]}]}]}]}]}]}]}]}]}]}]}]}]}]}]}')
    d.close()
    e = open(json_path, 'r')
    e.close()

    while True:
        try:
            with open(json_path) as fjson:
                data = json.load(fjson)
            break
        except ValueError:
            text_file = open(json_path, "r")
            text_string = text_file.read()
            text_file.close()
            text_string = text_string[:-1]
            text_file = open(json_path, "w")
            text_file.write(text_string)
            text_file.close()

    return json_path
