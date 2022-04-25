import os
from pickle import load


class CorpusTagging():

    file_path = None

    def __init__(self, path):
        self.file_path = path

    def tag(self):

        # load tagger
        try:
            input = open('custom_tagger.pkl', 'rb')
            tagger = load(input)
            input.close()
        except FileNotFoundError:
            return None

        # Create output file
        new_file_name = 'tagged_' + os.path.basename(self.file_path)
        tagged_file = open(new_file_name, mode='w+', encoding='UTF-8')

        file = open(self.file_path, mode='r', encoding='utf-8').readlines()

        for line in file:
            can_register = True
            new_line = ''
            tagged_sentence = tagger.tag(line.strip().split(' '))
            for token_tag in tagged_sentence:
                if token_tag[1] is not None:
                    new_line += token_tag[0] + '_' + token_tag[1] + ' '
                else:
                    can_register = False
                    break
            if can_register:
                tagged_file.write(new_line + '\n')
        tagged_file.close()

        return new_file_name
