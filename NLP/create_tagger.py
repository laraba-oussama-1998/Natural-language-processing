import re
from pickle import dump

import nltk


class Tagger:

    corpus_path = None

    def __init__(self, path):
        self.corpus_path = path

    def create_tagger(self):
        model = {}
        with open(self.corpus_path, mode='r', encoding='UTF-8') as lines:
            for line in lines:
                line_as_list = line.strip().split(' ')
                for token_tag in line_as_list:
                    data = re.match(r'(?P<token>.*)_(?P<tag>.*)', token_tag)
                    model[data['token']] = data['tag']

        custom_tagger = nltk.tag.UnigramTagger(model=model)
        # save model
        output = open('custom_tagger.pkl', 'wb')
        dump(custom_tagger, output, -1)
        output.close()

