"""
    A simple reader which reads plain noisy text.

    Author: Haobo Gu, Yuanhe Tian
    Date created: 04/15/2018
    Python version: 3.6.2
"""

import operator
import re
import os


def get_all_evaluation_files():
    raw_text_directory = "../data/OCR_text/"
    gold_standard_directory = "../data/gold_standard/"
    raw_file_path = []
    gold_file_path = []
    data_path1 = "Emma/"
    data_path2 = "newberry-mary-b-some-further-accounts-of-the-nile-1912-1913/"

    raw_path1 = raw_text_directory + data_path1
    gold_path1 = gold_standard_directory + data_path1

    raw_path2 = raw_text_directory + data_path2
    gold_path2 = gold_standard_directory + data_path2

    for i in range(1, 20):
        raw_file = raw_path1 + "eba-v" + str(i) + ".txt"
        gold_file = gold_path1 + "EBA-" + str(i) + ".txt"
        raw_file_path.append(raw_file)
        gold_file_path.append(gold_file)

    for i in range(0, 28):
        raw_file = raw_path2 + "NMB_" + str(i) + ".txt"
        gold_file = gold_path2 + "ESF_" + str(i) + ".txt"
        raw_file_path.append(raw_file)
        gold_file_path.append(gold_file)

    return raw_file_path, gold_file_path


def read_file(filename):
    """
    Read all contents in a file, and get a list of lines
    :type: filename: str
    :param: filename: name of the file
    :return: list of strings, one string per line
    """
    import codecs
    with codecs.open(filename, "r", encoding='utf-8', errors='ignore') as input_file:
        contents = input_file.read()
        contents = contents.split('\n')
    return contents


def clean_empty_line(raw_lines):
    """
    Clean all empty lines in the list and replace all whitespace character (\t\r\n\f) with a space
    :type raw_lines: list
    :param raw_lines: A list of strings need to be cleaned
    :return: a list of non-empty strings which can be split into tokens by space
    """
    no_empty_lines = []
    for raw_line in raw_lines:
        raw_line = raw_line.strip()
        raw_line = re.sub("\\s+", " ", raw_line)
        if operator.eq(raw_line, ""):
            continue
        else:
            no_empty_lines.append(raw_line)
    return no_empty_lines


def lines2string(lines):
    """
    Connect all strings in lines by a space
    :type lines: list[str]
    :param lines: A list of string to be connected
    :return: A string
    """
    content_string = ""
    for line in lines:
        content_string += line + " "
    content_string.strip()
    return content_string


def write_file(lines, filename):
    """
    Write a list of strings into a file
    :type lines: list[str]
    :param lines: a list of string to be written into file
    :type filename: str
    :param filename: the name of output file, the default name is ""cleaned_newberry-mary-b-some-further-accounts-of-the-nile-1912-1913.txt"
    """
    parent_dir = os.path.dirname(filename)
    if not os.path.exists(parent_dir):
        os.makedirs(parent_dir)
    output_file = open(filename, 'w', encoding='utf-8')
    for line in lines:
        output_file.write(line + "\n")


def get_pairs(ocr_file, gold_standard):
    """
    :type ocr_file: str
    :param ocr_file: path of raw oct text file, the default is "OCR_text/newberry-mary-b-some-further-accounts-of-the-nile-1912-1913.txt"
    :type gold_standard: str
    :param gold_standard: path of the gold standard file, the default is "gold_standard/Edit_ Some Further Accounts of the Nile 1912-1913.txt"
    :return: A tup whose first element is a string of raw text, and second element is a string of gold standard
    """
    raw_content = read_file(ocr_file)
    gold_content = read_file(gold_standard)
    r_content = clean_empty_line(raw_content)
    g_content = clean_empty_line(gold_content)
    return (lines2string(r_content), lines2string(g_content))

# Test script
if __name__ == "__main__":
    data_path = '../data/'
    output_path = "../output/"
    raw_text_file = "OCR_text/newberry-mary-b-some-further-accounts-of-the-nile-1912-1913.txt"
    cleaned_text_file = "cleaned_newberry-mary-b-some-further-accounts-of-the-nile-1912-1913.txt"
    gold_text_file = "gold_standard/Edit_ Some Further Accounts of the Nile 1912-1913.txt"
    raw_content = read_file(raw_text_file)
    gold_content = read_file(gold_text_file)
    r_content = clean_empty_line(raw_content)
    g_content = clean_empty_line(gold_content)
    # print(content)
    '''
    for item in content:
        tokens = nltk.tokenize.word_tokenize(item)
        print(item)
        print(tokens)
        print("")
    '''
    write_file(r_content)
    r_clean_string = lines2string(r_content)
    g_clean_string = lines2string(g_content)
    print("hello")
