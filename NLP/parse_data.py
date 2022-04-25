import os
import re
import time
from tkinter import END, messagebox
from import_tags import import_tags

import nltk

from calculate_weight import get_weight


class ParseData:

    def __init__(self, root, output, file):
        self.root = root
        self.output = output
        self.file = file

    def get_grammar_as_string(self):
        grammar_string = """"""
        grammar = open('grammar.txt', mode='r', encoding='UTF-8').readlines()
        for rule in grammar:
            grammar_string += rule

        return grammar_string

    def get_sentences_tags(self):

        import_tags(self.file)
        sentences_tags = []

        tags = open('tags.txt', mode='r', encoding='UTF-8').readlines()

        for tag in tags:
            sentences_tags.append(tag.strip().split(' '))

        os.remove('tags.txt')
        return sentences_tags

    def print_analyze(self, test_sentences_tags, rd_parser):

        self.output.config(state='normal')
        self.output.delete('1.0', END)
        i = 1

        precision = 0
        sum_of_weight = 0
        sum_of_weight_rf = 0

        for sentence in test_sentences_tags:

            self.output.insert(END, 'Analyse of sentence ' + str(i) + ' ... (the parsing may take a while, hold on)\n', 'tag')

            start = time.time()
            parsing_result = list(rd_parser.parse(sentence))
            process = time.time()
            print("holle")
            self.output.insert(END, str(parsing_result) + '\n')
            self.output.insert(END, 'Weight : ', 'tag')

            # weight
            weight = get_weight(sentence)
            self.output.insert(END, str(weight) + ' | ')

            sum_of_weight += weight

            # reward factor
            self.output.insert(END, 'RF : ', 'tag')
            reward_factor = self.get_reward_factor(sentence, parsing_result)
            self.output.insert(END, str(reward_factor))

            sum_of_weight_rf += reward_factor * weight

            self.output.insert(END, ' | ')
            self.output.insert(END, 'Time : ', 'tag')
            self.output.insert(END, str(process-start)+'\n')

            i += 1

        precision = sum_of_weight_rf / sum_of_weight
        self.output.insert(END, 'Precision : ', 'tag')
        self.output.insert(END, str(precision * 100) + ' % \n')


        self.output.config(state='disabled')

    def get_reward_factor(self, sentence, parsing_result):

        return 0 if len(parsing_result) == 0 else len(parsing_result[0].leaves()) / len(sentence)

    def parse(self):

        test_sentences_tags = self.get_sentences_tags()

        # Pass grammar to nltk parser
        grammar_string = self.get_grammar_as_string()
        grammar = nltk.CFG.fromstring(grammar_string)
        rd_parser = nltk.RecursiveDescentParser(grammar)

        # Print
        self.print_analyze(test_sentences_tags, rd_parser)
