from tkinter import *
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '../'))
import src.file_io as reader
import src.ntc as ntc
import src.ngram as ng
import re
import threading
import queue
from tkinter import filedialog
import codecs

class GUI:
    def __init__(self, master):
        self.master = master
        # Set widgets and layout
        self.correct_button = Button(master, width=10, text='correct', command=self.button_click)
        self.correct_button.grid(row=1, column=2)
        self.open_file_button = Button(master, width=10, text='open ...', command=self.open_file)
        self.open_file_button.grid(row=3, column=1, padx=10, pady=5)
        self.save_file_button = Button(master, width=10, text='save as ...', command=self.save_file)
        self.save_file_button.grid(row=3, column=3, padx=10, pady=5)
        self.input_text = Text(master, relief=GROOVE, height=20, width=60, borderwidth=2)
        self.input_text.insert(END, "Paste text here")
        self.master.bind_class("Text", "<Control-a>", self.select_all)  # rebind "select all" shortcut
        self.input_text.grid(row=0, column=1, rowspan=3, padx=10, pady=10)
        self.output_text = Text(root, relief=GROOVE, height=20, width=60, borderwidth=2)
        self.output_text.grid(row=0, column=3, rowspan=3, padx=10, pady=5)
        # Set correct model
        self.rbm = ntc.RuleBasedModel('ruleset')
        self.q = queue.Queue()
        model_path = "./model/"
        if 'model' in os.listdir('.'):
            model_path = "./model/"
        elif 'model' in os.listdir('..'):
            model_path = "../model/"
        else:
            print('can not find model folder')
            exit(0)
        self.statistic_model = ng.read_ngram_model(model_path, split_strategy=ng.TOKENIZER,
                                                   topN=50, delta=0.1, threshold=1.7, NE_list={})

    def open_file(self):

        input_filename = filedialog.askopenfilename()
        if input_filename != "":
            with codecs.open(input_filename, "r", encoding='utf-8', errors='ignore') as f:
                contents = f.read()
                self.input_text.delete('1.0', END)
                self.input_text.insert(END, contents)

    def save_file(self):
        ftypes = [('Plain texts', '*.txt'), ('All files', '*.*')]
        output_filename = filedialog.asksaveasfilename()
        parent_dir = os.path.dirname(output_filename)
        if not os.path.exists(parent_dir):
            os.makedirs(parent_dir)
        with open(output_filename, 'w', encoding='utf-8') as output_file:
            corrected_text = self.output_text.get("1.0", "end-1c")
            output_file.write(corrected_text)

    def select_all(self, event):
        # select text
        event.widget.tag_add("sel", "1.0", "end")

    def button_click(self):
        self.correct_button.configure(state=DISABLED)
        self.open_file_button.configure(state=DISABLED)
        self.save_file_button.configure(state=DISABLED)
        raw_text = self.input_text.get("1.0", "end-1c")
        self.output_text.delete('1.0', END)
        self.output_text.insert(END, "Processing, please wait ...")
        self.q = queue.Queue()
        ThreadedTask(self.q, self.rbm, self.statistic_model, raw_text).start()
        self.master.after(100, self.process_queue)

    def process_queue(self):
        try:
            msg = self.q.get(0)
            self.output_text.delete('1.0', END)
            self.output_text.insert(END, msg)
            self.correct_button.config(state=ACTIVE)
            self.open_file_button.configure(state=ACTIVE)
            self.save_file_button.configure(state=ACTIVE)
        except queue.Empty:
            self.master.after(100, self.process_queue)


class ThreadedTask(threading.Thread):
    def __init__(self, q, rbm, statistic_model, raw_text):
        threading.Thread.__init__(self)
        self.q = q
        self.rbm = rbm
        self.raw_text = raw_text
        self.statistic_model = statistic_model

    def run(self):
        lines = self.raw_text.split('\n')
        lines = reader.clean_empty_line(lines)
        result = []
        for line in lines:
            result.append(self.rbm.process(line))
        new_result = []
        for line in result:
            if not re.match("\\s+", line):
                new_line = ng.modify_line(self.statistic_model, line)
                new_result.append(new_line)
        corrected_text = ''
        for line in new_result:
            corrected_text = corrected_text + line + '\n'
        self.q.put(corrected_text)


root = Tk()
root.title('OCR Text Corrector')
main_ui = GUI(root)
root.mainloop()

