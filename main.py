import numpy as np
from sklearn.decomposition import PCA
import matplotlib.pyplot as plt
import nltk as nltk
#nltk.download('punkt')
from pathlib import Path
from text_classes import Text_tokenized
import plotly.express as px
import requests as rqst

verbose = False

#FUNCTIONS
def make_cooccurance_matrix(text_tokenized):
    matrix_dim = len(text_tokenized.vocabulary)
    cooccurance_matrix = np.zeros((matrix_dim, matrix_dim))
    for i in range(matrix_dim):
        for j in range(i, matrix_dim):
            if i == j:
                continue
            for s in text_tokenized.sentences_list:
                if text_tokenized.ordered_vocabulary[i].word_text in s.words_set and text_tokenized.ordered_vocabulary[j].word_text in s.words_set:
                    cooccurance_matrix[i][j] += 1
                    cooccurance_matrix[j][i] += 1
    return(cooccurance_matrix)

def compress_dimentions_PCA(matrix):
    pca_algorithm = PCA(n_components = 2)
    compressed_matrix = pca_algorithm.fit_transform(matrix)
    return compressed_matrix

def compile_points_list(compressed_matrix, text_class, user_chosen_words = []):
    words_points_list = []
    vocabulary_text = text_class.get_vocabulary_text()
    
    for w in user_chosen_words:
        for i in range(len(vocabulary_text)):
            if vocabulary_text[i] == w:
                words_points_list.append([compressed_matrix[i,0], compressed_matrix[i,1], w])

    #CUT N TOP WORDS
    return words_points_list

def input_user_words(vocabulary):
    user_chosen_words = []
    input_stop = False
    while input_stop == False:
        this_input = input('Choose a word from the vocabulary or write EXT to exit: ')
        if this_input == 'EXT':
            input_stop = True
            continue
        word_found = False
        for i in vocabulary:
            if i.word_text == this_input:
                word_found = True
                word_already_in_list = False
                for w in user_chosen_words:
                    if w == this_input:
                        word_already_in_list = True
                if word_already_in_list == True:
                    print('This word is already chosen for output')
                else:
                    print('Word ', this_input, ' chosen for output')
                    user_chosen_words.append(this_input)
        if word_found == False:
            print('No such word in the vocabulary')
    return user_chosen_words

def filter_by_word_pos(list_of_accepted_pos, accepted_words_percentage, text_class):
    user_chosen_words = []
    clipped_vocabulary = []
    clip_length = len(text_class.ordered_vocabulary)*accepted_words_percentage
    for i in range(int(clip_length)):
        clipped_vocabulary.append(text_class.ordered_vocabulary[i])
    for w in clipped_vocabulary:
        word_added = False
        for p in list_of_accepted_pos:
            if w.pos == p and word_added == False:
                user_chosen_words.append(w.word_text)
                word_added = True
    return user_chosen_words

def purge_words_from_output(user_chosen_words, words_to_purge):
    for w in words_to_purge:
        user_chosen_words.remove(w)




#START
txt = Path('nishe.txt').read_text()

nonwords = set({'.', '?', '!', ',', ':', ';', '-', '(', ')', '«', '»', '–', 'др'})
text = Text_tokenized(exceptions_list = nonwords, verbose = verbose)

text.parse_to_sentences(txt)
text.order_vocabulary()

#print(text.get_vocabulary_text())

cooccurance_matrix = make_cooccurance_matrix(text)




compressed_coocurance_matrix = compress_dimentions_PCA(cooccurance_matrix)


#user_chosen_words = input_user_words(text.vocabulary)

accepted_parts_of_speech = ['NOUN', 'ADJF', 'ADJS']
accepted_words_percentage = 0.3
unwanteds = []

user_chosen_words = filter_by_word_pos(accepted_parts_of_speech, accepted_words_percentage, text)
purge_words_from_output(user_chosen_words, words_to_purge = unwanteds)
print(user_chosen_words)


words_to_show_list = compile_points_list(compressed_coocurance_matrix, text,  user_chosen_words = user_chosen_words)
#words_to_show_list = np.array(words_to_show_list)
#print(words_to_show_list)

#SHOW POINTS

fig = px.scatter(x = [elem[0] for elem in words_to_show_list], y = [elem[1] for elem in words_to_show_list],
                 hover_name=[elem[2] for elem in words_to_show_list])
fig.show()

# list/dict/set generator