import json
import nltk


def get_count_uni_gram(unigram, uni_grams_frequency_dict):

    return uni_grams_frequency_dict[unigram]
    pass

def get_big_gram_cond(bi_gram, n_grams_frequency_dict, uni_grams_frequency_dict):
    """
    calculate the probability for the bigram (wi,wi-1) = count(wi-1wi) / count(wi-1)
    :param bi_gram: (wi-1, wi)
    :param n_grams_frequency_dict: list of all n-grams (n >= 2)
    :param uni_grams_frequency_dict : list of all uni-grams
    :return: conditional probability
    """

    return n_grams_frequency_dict[bi_gram] / uni_grams_frequency_dict[list(nltk.ngrams(bi_gram, 1))[0]]


def get_weight(sentence):

    # Load n-grams frequency from json file
    n_grams_frequency_dict_from_json = json.load(open('n-grams-frequency.json', 'r', encoding='UTF-8'))
    uni_gram_frequency_dict_from_json = json.load(open('uni-grams-frequency.json', 'r', encoding='UTF-8'))

    # Make keys as tuple instead of string
    n_grams_frequency_dict = {}
    uni_grams_frequency_dict = {}

    for n_gram, freq in n_grams_frequency_dict_from_json.items():
        n_grams_frequency_dict[eval(n_gram)] = freq

    for uni_gram, freq in uni_gram_frequency_dict_from_json.items():
        uni_grams_frequency_dict[eval(uni_gram)] = freq

    # Calculate weight

    weight = get_count_uni_gram(list(nltk.ngrams(sentence, 1))[0], uni_grams_frequency_dict)

    bi_grams = list(nltk.bigrams(sentence))

    for bi_gram in bi_grams:
        weight *= get_big_gram_cond(bi_gram, n_grams_frequency_dict, uni_grams_frequency_dict)

    return weight
