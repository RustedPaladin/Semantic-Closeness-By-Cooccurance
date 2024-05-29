import nltk as nltk
import pymorphy2
morph = pymorphy2.MorphAnalyzer()

class Text_tokenized:
    def __init__(self, exceptions_list, verbose = False):
        self.sentences_list = []
        self.vocabulary = []
        self.ordered_vocabulary = []
        self.iteration = 0
        self.exceptions_list = exceptions_list
        self.v = verbose

    def add_sentence(self, sentence_text):
        new_sentence = Sentence(sentence_text, self.exceptions_list)
        self.sentences_list.append(new_sentence)
        for i in new_sentence.words_set:
            self.add_word_to_vocabulary(i)
        
    def add_word_to_vocabulary(self, new_word_text):
        word_already_present = False
        for i in self.vocabulary:
            if i.word_text == new_word_text:
                if self.v == True: print('word ', new_word_text, ' present')
                word_already_present = True
                i.frequency += 1
        if word_already_present == False:
            if self.v == True: print('appending ', new_word_text)
            self.vocabulary.append(Word(new_word_text))
    
    def parse_to_sentences(self, input_text):
        list_of_sentences = nltk.tokenize.sent_tokenize(input_text)
        for i in list_of_sentences:
            self.add_sentence(i)
    
    def order_vocabulary(self):
        self.ordered_vocabulary = sorted(self.vocabulary, key=lambda x: x.frequency, reverse=True)

    def get_vocabulary_text(self):
        vocabulary_text_list = []
        for i in self.ordered_vocabulary:
            if self.v == True: vocabulary_text_list.append([i.word_text, i.frequency])
            else: vocabulary_text_list.append(i.word_text)
        return vocabulary_text_list
    

    def get_strings_from_sentences_to_list(self):
        list = []
        for i in self.sentences_list:
            list.append(i.text)
        return list

class Sentence:
    def __init__(self, sentence_text, exceptions_list):
        self.text = sentence_text
        self.words_set = set({})
        new_words = nltk.word_tokenize(sentence_text)
        for w in new_words:
            if w not in exceptions_list:
                normalized_word = morph.parse(w)[0].normal_form
                self.words_set.add(normalized_word)
        #print('set of words is ', self.words_set)

class Word:
    def __init__(self, word_text):
        self.forms = [word_text.lower()]
        self.word_text = self.forms[0]
        self.frequency = 1
        self.pos = morph.parse(word_text)[0].tag.POS
        #print(self.word_text, 'is a ', self.pos)