import sys

import nltk



def is_subset(small_set, big_set):
    """

    :param small_set: list
    :param big_set: list
    :return: True if big_set contains strict small_set, False else
    """

    if small_set == big_set:
        return False

    count = 0
    k = 0
    for i in range(0, len(big_set)):
        if big_set[i] == small_set[0]:
            k = i + 1
            count = 1
            for j in range(1, len(small_set)):
                if k < len(big_set):
                    if big_set[k] == small_set[j]:
                        count += 1
                        if count == len(small_set):
                            return True
                        k += 1
                    else:
                        break

    return True if count == len(small_set) else False


def start_from(i, big, small):

    """
    :param i: starting index
    :param big: the list containing small (we suppose small exists in big and it's strict smaller)
    :param small: the sequence to look up it starting position in big
    :return: true if small starts from index i, false else
    """

    all_match = True
    small_index = 0
    k = i

    while small_index < len(small) and k < len(big):
        if small[small_index] != big[k]:
            return False
        small_index += 1
        k += 1

    return all_match


def substitute(replace, replace_by, replace_in):
    """
    :param replace: the subsequence to be replaced
    :param replace_by: the sequence that will replace the replace input
    :param replace_in: the big sequence
    :return:
    """

    replace_list = list(replace)
    replace_in_list = list(replace_in)
    result = []
    done = False
    i = 0
    while i < len(replace_in_list):
        # Check existence starting from i
        if start_from(i, replace_in_list, replace_list) and not done:
            # the sequence starts from i
            result.append(replace_by)
            i = i + len(replace_list)
            done = True
        else:
            result.append(replace_in_list[i])
            i += 1


    return tuple(result)


def generate_grammar_structure(freq_dist):
    """
    :param freq_dist: nltk.FreqDist dictionnary of n_grams
    :return: data structure to accelerate substitution step
    """

    # Sort n_grams to extract max from top of list, thus, reducing complexity
    sorted_dic = sorted(freq_dist.items(), key=lambda item: item[1], reverse=True)

    grammar = {}
    non_terminal_dict = {}
    i = 1
    total_size = len(sorted_dic)

    while len(sorted_dic) > 0:

        # Find the max
        max_n_gram = sorted_dic[0][0]

        # Delete it
        del sorted_dic[0]

        non_terminal_symbol = 'X' + str(i)

        grammar[max_n_gram] = {
            'non_terminal': non_terminal_symbol,
            'sub_list': []
        }

        non_terminal_dict[non_terminal_symbol] = max_n_gram

        size = len(max_n_gram)

        if size > 2:
            # Generate n_grams for this n_gram
            for j in range(size - 1, 1, -1):
                i_grams = list(nltk.ngrams(max_n_gram, j))
                # Check if max_n_gram contain production of small non_terminals
                for i_gram in i_grams:
                    if i_gram in grammar and is_subset(i_gram, max_n_gram):
                        # Add this non-terminal to i_gram substitution list
                        grammar[i_gram]['sub_list'].append(non_terminal_symbol)

                        # Modify max_n_gram to avoid collisions and conflicts between rules
                        max_n_gram = substitute(i_gram, '', max_n_gram)

        # sys.stdout.write("\r" + str(i) + ' / ' + str(total_size) + ' N-gram processed without substitution')
        # sys.stdout.flush()
        i += 1

    # print('\n')

    return non_terminal_dict, grammar


def generate_grammar_rules(freq_dist):
    """
    :param freq_dist: n-grams resulted from previous step (n-gram generation)
    :return:
    The frequency distribution dictionary is sorted with descended order
    The n-gram with highest frequency is on the top of the list (O(1) complexity retrieval)
    The n-gram is removed from the frequency distribution with O(1) complexity
    Making substitution in grammar_rules_without_substitution dictionary
    """

    grammar_rules_without_substitution, data_structure = generate_grammar_structure(freq_dist)

    total_size = len(grammar_rules_without_substitution)
    i = 1

    for i_gram in data_structure:
        non_terminal = data_structure[i_gram]['non_terminal']
        sub_list = data_structure[i_gram]['sub_list']

        for sub_non_terminal_where in sub_list:
            replace_in = grammar_rules_without_substitution[sub_non_terminal_where]
            grammar_rules_without_substitution[sub_non_terminal_where] = substitute(i_gram, non_terminal, replace_in)

        # sys.stdout.write("\r" + str(i) + ' / ' + str(total_size) + ' N-gram processed with substitution')
        # sys.stdout.flush()
        i += 1

    return grammar_rules_without_substitution


