def generate_free_context_grammar(grammar_rules):
    grammar_string = ''''''
    S = 'S -> '
    for non_terminal, terminals in (grammar_rules.items()):
        # S += non_terminal + ' | '
        grammar_string += 'S -> ' + non_terminal + '\n'

    # grammar_string = S[:-2] + '\n'

    for non_terminal, terminals in (grammar_rules.items()):
        grammar_string += non_terminal + ' -> '
        for terminal in terminals:
            if terminal not in grammar_rules.keys():
                grammar_string += '"' + terminal + '" '
            else:
                grammar_string += terminal + ' '
        grammar_string += '\n'

    file = open('grammar.txt', mode='w+', encoding='UTF-8')
    file.write(grammar_string)


