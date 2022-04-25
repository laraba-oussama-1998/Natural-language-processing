# Description

This application aims to induce grammar for any particular language using a large fully tagged  
corpus.
Tne approach is inspired from the paper : Selab, E., and Guessoum, A. (2015). A statistical approach for the induction of a grammar of Arabic, In: 2015 IEEE/ACS 12th International Conference of Computer Systems and Applications (AICCSA), Marrakech, Morocco, pp. 1-8. doi:10.1109/AICCSA.2015.7507250.

# Installation 

This project is open source, just lunch the main.py to run the application


# Contribution 

This project was made by 2 students in USTHB university

-- MEGHNI Mohamed El Amine
-- Laraba Oussame



# Files

-- main.py : entery point of application

--calculate_weight.py : script used to calculate the weight of a given test sentence

-- create_tagger.py : script used to create a tagger based on a tagged corpus

-- custom_tagger.pkl : tagger generated with the script create_tagger.py (should be saved away to avoid overwrite)

-- generate_grammar.py : main script that generate grammar

-- generate_grammar_rules.py : script used to generate grammar rules (given n-grams as input)

-- import_tags.py : script used to extract tags only from the corpus and save them into tags.txt file

-- generate_n_grams.py : script used to generate n-grams (given tags.txt as input)

-- grammar.txt : induced grammar (should be saved away to avoid overwrite)

-- gui.py : script that create user interface

-- n-grams-frequency.json : this file contains frequency distribution of all n-grams, those data are used
to compute evaluation (should be saved away to avoid overwrite)

-- parse_data.py : script used to parse test data

-- tag_corpus.py : script used to tag a corpus and extract the tagged version on tagged_[CORPUS_NAME].txt file

-- uni-grams-frequency.json : this file contains frequency distribution of all uni-grams, those data are used to compute evaluation (should be saved away to avoid overwrite)
