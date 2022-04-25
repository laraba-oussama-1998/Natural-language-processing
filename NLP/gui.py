import re
import time
from pickle import dump, load
from threading import Thread
from tkinter import Tk, filedialog, Text, END, Label, messagebox
from tkinter.ttk import Style, Button
import os
import nltk
from generate_grammar import GrammarGeneration
from parse_data import ParseData
from create_tagger import Tagger
from tag_corpus import CorpusTagging


class GUI:
    import_train_data_button = None
    import_test_data_button = None
    create_tagger_button = None
    tag_corpus_button = None
    output_1 = None
    output_2 = None

    def __init__(self):
        """
        Initialize UI window
        """
        self.root = Tk()
        self.root.title('NLP - Grammar Generator')
        self.root.state("zoomed")
        self.build()

    def show(self):
        """
        Show main UI to the user
        :return:
        """
        self.root.mainloop()

    def build(self):
        """
        Insert UI components to the main window
        :return:
        """

        # input_text = Label(self.root, 'H')
        # input_text.place(x=100,y=200)

        Style().configure(style='TButton', font=('poppins light', 11))

        self.import_train_data_button = Button(self.root, text='Import data to analyze', width=20,
                                               command=self.import_test)
        self.import_test_data_button = Button(self.root, text='Generate grammar', width=20,
                                              command=self.import_train_data)

        self.create_tagger_button = Button(self.root, text='Create tagger', width=20,
                                           command=self.create_tagger)

        self.tag_corpus_button = Button(self.root, text='Tag a corpus', width=20,
                                        command=self.tag_corpus)

        self.output_1 = Text(self.root, width=125, height=10)
        self.output_1.config(font=("poppins", 10), state='disabled')
        self.output_2 = Text(self.root, width=125, height=10)
        self.output_2.config(font=("poppins", 10), state='disabled')
        self.output_1.tag_configure("tag", foreground="#0288d1")
        self.output_2.tag_configure("tag", foreground="#0288d1")
        self.output_1.tag_configure("success", foreground="#43a047")
        self.output_2.tag_configure("success", foreground="#43a047")

        input_label = Label(text='Input data', font=('poppins', 16))
        output_label = Label(text='Output data', font=('poppins', 16))

        self.import_train_data_button.place(x=20, y=30)
        self.import_test_data_button.place(x=20, y=100)
        self.create_tagger_button.place(x=20, y=170)
        self.tag_corpus_button.place(x=20, y=240)

        self.output_1.place(x=300, y=50)
        self.output_2.place(x=300, y=350)

        input_label.place(x=300, y=5)
        output_label.place(x=300, y=300)

    def print_input_data(self, message):

        self.root.filename = filedialog.askopenfilename(initialdir=".", title="Select file")

        if self.root.filename != '':

            if message is not None:
                self.output_2.config(state='normal')
                self.output_2.delete('1.0', END)
                self.output_2.insert(END, message, 'tag')
                self.output_2.config(state='disabled')

            f = open(self.root.filename, encoding='UTF-8')

            self.output_1.config(state='normal')
            self.output_1.delete('1.0', END)
            i = 1
            for line in f:
                self.output_1.insert(END, 'Sentence ' + str(i) + '\n', 'tag')
                self.output_1.insert(END, line)
                i += 1
            self.output_1.config(state='disabled')

    def create_tagger(self):

        t1 = Thread(target=self.create_tagger_thread).start()

    def create_tagger_thread(self):

        start = time.time()
        self.print_input_data(message='Processing corpus, this may take a while ... please wait\n')
        if self.root.filename != '':
            Tagger(self.root.filename).create_tagger()
            self.output_2.config(state='normal')
            self.output_2.delete('1.0', END)
            self.output_2.insert(END, 'Tagger successfully generated !' + '\n', 'success')
            self.output_2.config(state='disabled')
            messagebox.showinfo(title='Process finished',
                                message='Tagger successfully created and saved as custom_tagger.pkl file. Time : %0.2f sec' % (
                                        time.time() - start))

    def tag_corpus(self):

        t1 = Thread(target=self.tag_corpus_thread()).start()

    def tag_corpus_thread(self):

        # check if tagger exists
        try:
            open('custom_tagger.pkl', 'rb')
            self.print_input_data(message='Processing corpus, this may take a while ... please wait\n')
            if self.root.filename != '':
                start = time.time()
                file_name = CorpusTagging(self.root.filename).tag()
                end = time.time()
                self.output_2.config(state='normal')
                self.output_2.delete('1.0', END)
                tagged_file = open(file_name, mode='r', encoding='UTF-8')
                i = 1
                for line in tagged_file:
                    self.output_2.insert(END, 'Sentence ' + str(i) + '\n', 'tag')
                    self.output_2.insert(END, line)
                    i += 1
                self.output_2.config(state='disabled')

                messagebox.showinfo(title='Process finished',
                                    message='Corpus successfully tagged and extracted in ' + file_name + 'file. Time : '
                                                                                                         '%0.2f sec' % (
                                                    end - start))
        except FileNotFoundError:
            messagebox.showerror(title='Tagging error',
                                 message='Cannot find tagger, maybe you need to create a tagger to handle no tagged '
                                         'corpus')

    # T E S T
    def import_test(self):
        t1 = Thread(target=self.lunch_test_thread).start()

    def lunch_test_thread(self):

        self.print_input_data(message=None)
        # check if grammar exists
        try:
            open('grammar.txt', mode='r', encoding='UTF-8')
            if self.root.filename != '':
                ParseData(self.root, self.output_2, self.root.filename).parse()
        except FileNotFoundError:
            messagebox.showerror("Error", "Grammar.txt file not found, please generate a grammar to continue")

    # T R A I N
    def import_train_data(self):
        t1 = Thread(target=self.lunch_train_thread).start()

    def lunch_train_thread(self):
        self.print_input_data(message='Grammar generation in progress ... please wait, this may take a while')
        if self.root.filename != '':
            grammar_generation = GrammarGeneration(self.root, self.output_2, self.root.filename)
            grammar_generation.generate()
