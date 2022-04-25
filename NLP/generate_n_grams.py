import json
import os
from tkinter import messagebox

import nltk


""" Generate the n-grams for each sentence in tags
For each sentence's tags, we generate the n-grams starting from n = 2 to the length of the sentence
"""


def generate_n_grams():

    tags = open('tags.txt', mode='r', encoding='UTF-8').readlines()
    n_grams = nltk.FreqDist()
    uni_grams = nltk.FreqDist()
    i = 1
    for sentence_tags in tags:

        tags_as_list = sentence_tags.strip().split(' ')

        if None not in tags_as_list and len(tags_as_list) > 1:
            for i in range(2, len(tags_as_list) + 1):
                sentence_n_grams = list(nltk.ngrams(tags_as_list, i))
                for n_gram in sentence_n_grams:
                    if n_gram in n_grams:
                        n_grams[n_gram] += 1
                    else:
                        n_grams[n_gram] = 1

            uni_grams_list = list(nltk.ngrams(tags_as_list, 1))
            for n_gram in uni_grams_list:
                if n_gram in uni_grams:
                    uni_grams[n_gram] += 1
                else:
                    uni_grams[n_gram] = 1

    os.remove('tags.txt')


    if len(n_grams) == 0:
        messagebox.showerror(title='Tagging error',
                             message='Cannot handle given corpus (some sentences are not fully tagged maybe)')
        exit()




    saved_dict_n_grams = {}
    for key, value in n_grams.items():
        saved_dict_n_grams[str(key)] = value

    saved_dict_uni_grams = {}
    for key, value in uni_grams.items():
        saved_dict_uni_grams[str(key)] = value

    with open('n-grams-frequency.json', 'w', encoding='UTF-8') as file_writer:
        json.dump(saved_dict_n_grams, file_writer, ensure_ascii=False, sort_keys=False)

    with open('uni-grams-frequency.json', 'w', encoding='UTF-8') as file_writer:
        json.dump(saved_dict_uni_grams, file_writer, ensure_ascii=False, sort_keys=False)


    return n_grams
