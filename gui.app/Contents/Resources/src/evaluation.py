"""
Provides evaluation methods for OCR correction result.

    Author: Haobo Gu
    Date created: 04/24/2018
    Python version: 3.6.2
"""

import src.wer as wer
import re

def evaluate(result_string, gold_string, print_alignment=False):
    """
    Evaluate system's performance using word error rate or rouge measurement.
    Use 'wer' and 'rouge' to specify which measurement you're going to use.
    :type result_string: str
    :type gold_string: str
    :rtype: float list
    """
    # re_seq = nltk.word_tokenize(result_string)
    # gold_seq = nltk.word_tokenize(gold_string)
    gold_string = re.sub('’', '\'', gold_string)
    re_seq = result_string.split(' ')
    gold_seq = gold_string.split(' ')
    new_re_seq = []
    for word in re_seq:
        if word != '':
            new_re_seq.append(word)
    new_gold_seq = []
    for word in gold_seq:
        if word != '':
            new_gold_seq.append(word)

    wer_calculator = wer.WERCalculator(new_gold_seq, new_re_seq)
    wer_calculator.set_diff_stats(prepare_alignment=True)
    if print_alignment:
        wer_calculator.print_alignment()

    return wer_calculator.wer()

