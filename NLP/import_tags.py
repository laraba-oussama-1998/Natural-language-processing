import re
from pickle import load
from tkinter import messagebox

''' 
Import sentence's tags from tagged corpus
'''


def import_tags(file_path):
    lines = open(file_path, encoding='UTF-8')
    tags = open('tags.txt', mode='w+', encoding='UTF-8')

    # load tagger
    try:
        input = open('custom_tagger.pkl', 'rb')
        tagger = load(input)
        input.close()
        # check if corpus is tagged / no
        for line in lines:
            words_tags = line.split()
            tags_sentence = []
            if len(words_tags) > 1:
                for token_tag in words_tags:
                    data = re.match(r'(?P<token>.*)_(?P<tag>.*)', token_tag)
                    if data is None:
                        # Tag the word
                        tags_sentence.append(tagger.tag([token_tag])[0][1])
                    else:
                        tags_sentence.append(data['tag'])
                try:
                    tags.write(' '.join(tags_sentence) + '\n')
                except TypeError:
                   pass

    except FileNotFoundError:
        messagebox.showerror(title='Tagging error',
                             message='Cannot find tagger, maybe you need to create a tagger to handle no tagged corpus')
        exit()
