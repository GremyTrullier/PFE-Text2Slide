import tkinter as tk
import tkinter.filedialog as tkf

from nlp2pptx import nlp2pptx
from doc2json import doc2json
from json2nlp import json2nlp


class Application(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.master.geometry("500x200")
        self.master.title('Text2Slide')
        self.master.iconbitmap('./text2slide.ico')
        self.pack()
        self.file_path = ''

        self.input_file_button = tk.Button(self.master, text='Choose file', command=self.choose_file, height=1, width=15)
        self.input_file_button.place(x=50, y=150)

        self.convert_button = tk.Button(self.master, text='Convert into pptx', command=self.return_path, height=1, width=15)
        self.convert_button['state'] = 'disable'
        self.convert_button.place(x=340, y=150)

        self.input_file_label = tk.Label(self.master, text=self.file_path, height=1, width=150)
        self.input_file_label.pack()

        self.nlp_type_text = tk.Label(self.master, text="Summarization type :", height=1, width=150)
        self.nlp_type_text.pack()

        OPTION_LIST = [
            "KeyConcept",
            "KeySentence",
            "KeyWord"
        ]
        self.nlp_type = tk.StringVar(self.master)
        self.nlp_type.set(OPTION_LIST[0])
        self.nlp_type_box = tk.OptionMenu(self.master, self.nlp_type, *OPTION_LIST)
        self.nlp_type_box.place(x=190, y=50)

    def choose_file(self):
        self.file_path = tkf.askopenfilename(
            parent=self.master, initialdir='C:',
            title='Choose file',
            filetypes=[('Word Documents', '.docx')])
        self.input_file_label['text'] = self.file_path
        self.convert_button['state'] = 'normal'

    def return_path(self):
        self.convert_button['state'] = 'disable'
        self.input_file_button['state'] = 'disable'
        self.nlp_type_box['state'] = 'disable'
        pipeline(self.file_path, self.nlp_type.get())


def startapp():
    root = tk.Tk()
    app = Application(master=root)
    app.mainloop()


def pipeline(file_path, nlp_type):
    json_path = doc2json(file_path)
    nlp_path = json2nlp(json_path, nlp_type)
    nlp2pptx(nlp_path)


if __name__ == '__main__':
    startapp()
