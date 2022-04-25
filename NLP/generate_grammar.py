import time
from tkinter import END, messagebox

import nltk

from convert_grammar_to_string import generate_free_context_grammar
from generate_grammar_rules import generate_grammar_rules
from generate_n_grams import generate_n_grams
from import_tags import import_tags


class GrammarGeneration:
    file_path = None
    output = None
    root = None

    def __init__(self, root, output, file_path):
        self.file_path = file_path
        self.output = output
        self.root = root
        pass

    def print_grammar(self, grammar):

        self.output.config(state='normal')

        self.output.delete('1.0', END)
        grammar_as_list = grammar.split('\n')

        for production in grammar_as_list:
            self.output.insert(END, production + '\n')

        self.output.config(state='disabled')


    def generate(self):
        start = time.time()

        # Import tags
        tags = import_tags(self.file_path)

        # Generate n-grams from tags
        n_grams = generate_n_grams()

        # Generate grammar rules
        grammar_rules = generate_grammar_rules(n_grams)

        # Generate the Context free grammar for this grammar rules
        generate_free_context_grammar(grammar_rules)

        self.output.config(state='normal')
        self.output.delete('1.0', END)
        self.output.insert(END, 'Grammar successfully generated !' + '\n', 'success')
        self.output.config(state='disabled')

        messagebox.showinfo(title='Process finished',
                            message='Grammar successfully induced and extracted. Time : %0.2f sec' % (time.time() - start))
