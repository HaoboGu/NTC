"""
    Noisy text correction module
"""
import os
import re
import string
from operator import itemgetter
import nltk

def nth_repl(s, sub, repl, nth):
    """
    Replace n-th substring in s to repl. Return replaced s.
    :param s: str
    :param sub: str
    :param repl: str
    :param nth: int
    :return: str
    """
    find = s.find(sub)
    # if find is not p1 we have found at least one match for the substring
    i = find != -1
    # loop util we find the nth or we find no match
    while find != -1 and i != nth:
        # find + 1 means we start at the last match start index + 1
        find = s.find(sub, find + 1)
        i += 1
    # if i  is equal to nth we found nth matches so replace
    if i == nth:
        return s[:find]+repl+s[find + len(sub):]
    return s


class RuleBasedModel:
    def __init__(self, ruleset_folder):
        """
        :param ruleset_folder: the folder name
        """
        self.char_rules = {}
        self.vocabulary = set()  # set of unigrams
        self.long_vocabulary = set()  # set of long vocabulary
        self.unigram = {}  # dict of unigrams
        self.place_names = []
        self.personal_names = []
        self.dis_bigrams = []
        self.chars = string.ascii_letters
        self.puncs = string.punctuation
        self.numbers = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '0']

        if ruleset_folder in os.listdir('.'):
            self.path = './' + ruleset_folder
        elif ruleset_folder in os.listdir('..'):
            self.path = '../' + ruleset_folder
        else:
            print('Wrong rule set folder name!')
            exit(0)
        self.read_char_rule_and_vocab()

    def read_char_rule_and_vocab(self):
        """
        Read char rules and vocabularies in to rule-based model.
        """
        ruleset_list = ['CharRules.txt', 'vocabulary.txt', 'PlaceNames.txt', 'PersonalNames.txt',
                        'unigram.txt', 'words_long.txt']
        for filename in ruleset_list:
            file_path = os.path.join(self.path, filename)
            ruleset = {}
            voc = []
            unigram_dict = {}
            with open(file_path, 'r', encoding='utf-8') as r_f:
                content = r_f.read()
                rule_list = content.split('\n')
                # If not vocabulary
                if filename not in ['vocabulary.txt', 'PlaceNames.txt', 'PersonalNames.txt',
                                    'DisambigTwograms.txt', 'unigram.txt', 'words_long.txt']:
                    for rule in rule_list:
                        elements = rule.split(';')
                        if int(elements[2]) > 10:
                            if elements[1] in ruleset:
                                ruleset[elements[1]] = ruleset[elements[1]] + [(elements[0], elements[2])]
                            else:
                                ruleset[elements[1]] = [(elements[0], elements[2])]  # Store rule using dictionary
                    self.char_rules = ruleset
                else:
                    # Read vocabulary
                    for word in rule_list:
                        if filename == 'DisambigTwograms.txt':
                            voc.append(word.strip('\n').split('\t')[0])
                        elif filename == 'unigram.txt':
                            unigram, count = word.strip('\n').split(' ')[0].lower(), int(word.strip('\n').split(' ')[1])
                            unigram_dict[unigram] = count
                            voc.append(unigram)
                        else:
                            voc.append(word.strip('\n').split(' ')[0].lower())
                    if filename == 'unigram.txt':
                        self.vocabulary = set(voc)
                        self.unigram = unigram_dict
                    elif filename == 'vocabulary.txt':
                        self.long_vocabulary = self.long_vocabulary.union(set(voc))
                    elif filename == 'PlaceNames.txt':
                        self.place_names = set(voc)
                    elif filename == 'PersonalNames.txt':
                        self.personal_names = set(voc)
                    elif filename == 'DisambigTwograms.txt':
                        self.dis_bigrams = set(voc)

    def remove_garbage_strings(self, text):
        """
        Remove garbage strings and garbage lines
        :param text: string
        :return: string
        """
        n_punc = 0
        punc_set = set()
        for char in text:
            if char not in self.chars and char is not ' ' and char not in self.numbers:
                # Puncts
                n_punc += 1
                punc_set.add(char)
        if n_punc / len(text) > 0.5 and len(punc_set) >= 3:
            # A string consists of many random punctuations
            text = "[Deleted line]"
        else:
            word_seq = text.split(' ')
            for word in word_seq:
                if self._is_garbage(word):
                    text = text.replace(word, '____')
        return text

    def _is_garbage(self, word):
        count = 0
        if len(word) <= 0:
            return False
        if len(word) > 40:
            return True
        n_punc = 0
        punc_set = set()
        if len(word) > 2:
            for char in word[1:-1]:
                if char not in self.chars and char is not ' ' and char not in self.numbers:
                    # Punctuations
                    n_punc += 1
                    punc_set.add(char)
        if count/len(word) > 0.5 and len(punc_set) >= 3:
            return True
        return False

    def new_apply_char_rule(self, text):
        """
        Apply character based correction rule on text
        :param text: str
        :return: str
        """
        word_seq = nltk.word_tokenize(text)
        for word in word_seq:
            word = re.sub('^\W+$', '', word)
            if word not in self.vocabulary and word.lower() not in self.vocabulary and word != ''\
                    and word not in self.long_vocabulary and word.lower() not in self.long_vocabulary:
                candidates = []  # list of (replaced word, word freq, rule freq)
                for key, target_ch_list in self.char_rules.items():
                    # For rules correcting key
                    if key in self.chars:
                        # for all regular letters, find all occurrences in the word
                        n_subs = len(re.findall(key, word))  # find how many keys found in word
                    elif key in word:
                        # for other puncs and numbers, only substitute once
                        n_subs = 1
                    else:
                        n_subs = 0
                    if n_subs > 0:
                        for target_ch, count in target_ch_list:
                            for i in range(n_subs):
                                replaced = nth_repl(word, key, target_ch, i+1)  # replace n-th letter
                                if replaced in self.vocabulary or replaced.lower() in self.vocabulary:
                                    # Add replaced word and rule's count to candidates
                                    if replaced in self.unigram:
                                        candidates.append((replaced, self.unigram[replaced], count))
                                    elif replaced in self.long_vocabulary:
                                        candidates.append((replaced, 1, count))
                if len(candidates) <= 0 or len(word) <= 1:
                    continue
                else:
                    candidates = sorted(candidates, key=itemgetter(2), reverse=True)
                    candidates = sorted(candidates, key=itemgetter(1), reverse=True)
                    if not candidates[0][0][0].isupper():
                        corrected_word = candidates[0][0].lower()
                    else:
                        corrected_word = candidates[0][0]
                    if word.startswith('*'):
                        word = word.replace("*", "\*", 1)
                    p1 = ' ' + word + ' '
                    p2 = ' ' + word + '$'
                    p3 = '^' + word + ' '
                    # print(corrected_word)
                    text = text.replace(p1, ' ' + corrected_word + ' ')
                    text = re.sub(p2, ' ' + corrected_word, text)
                    text = re.sub(p3, corrected_word + ' ', text)
        return text

    def merge_words(self, text):
        """
        Merge adjacent tokens if they can form a word
        :param text: str
        :return: str
        """
        word_seq = text.split(' ')
        n_word = len(word_seq)
        for i in range(n_word-1):
            first_word = word_seq[i]
            second_word = word_seq[i+1]
            if first_word.lower() not in self.unigram and second_word.lower() not in self.unigram:
                # Both words are not in the unigram
                merged_word = first_word + second_word
                if merged_word.lower() in self.unigram or merged_word.lower() in self.vocabulary:
                    text = text.replace(first_word + ' ' + second_word, merged_word)
                    print(first_word + ' ' + second_word, '->', merged_word)
        return text

    def correct_case(self, text):
        """
        If a word starts with a character in lower case, then lower the entire word
        :param text: str
        :return: str
        """
        word_seq = text.split(' ')
        for word in word_seq:
            if word[0].islower():
                text = text.replace(word, word.lower())
        return text

    def process(self, text):
        # main method to process noisy text

        # Apply rules first
        text = self.merge_words(text)
        text = self.remove_garbage_strings(text)
        text = self.new_apply_char_rule(text)
        text = self.correct_case(text)
        return text


# Test script
if __name__ == '__main__':
    rule_model = RuleBasedModel('ruleset')
    rule_model.read_char_rule_and_vocab()
    print(rule_model.unigram)
    # ntc = NoisyTextCorrection(rule_model)
    # cr = ntc.apply_char_rule('Darling Gopher -The day we got to Naples Wns simply henvenly. I posted you a letter from there the minute I reached the Hotel.')


