# Technical documentation for NTC

This document contains technical details of OCR post-correction system NTC. This document is developed for the people who want to know the implementation details or do future developments based on this project. 

## System Architecture

This project consists of five main parts: input/output, rule-based module, statistical based module, evaluation module, GUI module. 

## Input & Output

Input/Output module is implemented in `src/file_io.py`.

Input/Output module contains functions used for reading input plain text files and writing system output in plain text form. Input/Output module also contains functions used to clean and convert data

#### Main functions

- `read_file`: read a plain text file, return a list of lines
- `clean_empty_line`: remove empty lines in a list of lines
- `lines2string`: connect a list of string to one string
- `write_file`: write a list of string to output file

## Rule-based system

Rule-based correction module is implemented in `src/ntc.py`.

The main class is `RuleBasedModel` class, which takes the name of ruleset folder as the initial argument. The  class will automatically read vocabulary and character rules when initializing. 

The class also provide a pipeline procedure for automatically apply rule-based correction on a string, which contains merging adjacent words, removal of garbage strings and character rule-based correction: just use the following python script: 

```python
import src.ntc as rb

rule_model = rb.RuleBasedModel('ruleset')
corrected_text = rule_model.process("input text here")
```

### Ruleset

Some rulesets are required in this module.  Rulesets are in the `ruleset` folder in root directory. A number of rulesets are available in this project, but for now, only character based rules are used.

Most of rulesets come from Tedunderwood's [DataMunging project](https://github.com/tedunderwood/DataMunging). 

### Character based correction

The main correction method in rule-based module is charachter based correction. Character based correction uses ruleset in `ruleset/CharRules.txt`. 

The character based correction is implemented in `RuleBasedModel.new_apply_char_rule()`. 

For each wrong word in the text, the correction function generates a candidate list by trying to apply all character rules. If the generated word is in the vocabulary, then add this word to the candidate list. After all rules are tried, the best word will be selected according to the occurrence of this word in training data. If there is a tie, the occurrence of the corresponding rule will be used as the evidence. 

### Merge adjacent words

You can use `RuleBasedModel.merge_words()` to merge adjacent words to one word if two adjacent words are not in the vocabulary and merged word is in the vocabulary.  

### Remove garbage strings

You can use  `RuleBasedModel.remove_garbage_strings()` to remove meaningfulless strings in the text. There are several rules for identifying garbage strings. For details, you can check [Kazem TAGHVA's paper](https://pdfs.semanticscholar.org/94aa/36ce7216a3c86f3040e53b4c13fe66e1ef4f.pdf).

## Statistical system

Statistical correction module is implemented in `src/ngram.py	`. The main idea of statistical correction is to maximize the overall probability of the sentence. 

The main procedure of statistical correction is:

1. Words that don't appear in vocabulary or training corpus will be considered a 'wrong' word;
2. Calculate the Edit Distances between the 'wrong' word and words in vocabulary (training corpus) whose length is no more larger or smaller 1 than the length of the 'wrong' word;
3. Choose top 50 similar words with lowest Edit Distance as the candidates, and the 'wrong' word itself will also be taken into count;
4. Choose the best word which gives the maximum probability of the sentence in bigram language model. 

### Training Corpus

The training corpus is under `./data/` directory. If you want to train the model on you own corpus, you can to delete all files under `historical_corpus` and `other_corpus` directory and move your files under `other_corpus` folder (we recommend you to backup all files). Then train the model using the following code in command line:

```shell
python3 src/train.py
```

You can also add the following code into your script to train the model:

```python
ngram.ngrammodel(data_path, model_path, split_strategy=ngram.TOKENIZER, modern_corpus=False)
```

After training, two files will be created under `./model/` which store the data for n-gram model. Our program will read the trained model files, so you only need to train the model once on your corpus. 

### N-gram model

Class `ngram_model` stores parameters used in ngram model

### Edit Distance

A modified version of Levenshtein distance is used to measure the similarity between words. You can use `wf_levenshtein(word1, word2)` to calculate Levenshtein distance. 

For details of Levenshtein distance, please check [here](https://en.wikipedia.org/wiki/Levenshtein_distance).

In our project, we use 0.8 as the score for substitution. 

### Viterbi algorithm

The sentence probability is calculated using Viterbi algorithm, which is implemented in `bestoutput() ` function. 

## Evaluation system

### Word error rate calculation

We use word error rate as our evaluation method. The script for calculating word error rate comes from our classmate Jimmy. You can check their project [here](https://github.com/Linguistics575/575_OCR).

If you want to calculate word error rate of two strings, just use `evaluate()` function in `evaluation.py`. 

### Test data & gold standard

Test data and gold standard are stored in `data` folder. In `data` folder, raw OCR text is in `OCR_text` folder, gold standard is in `gold_standard` folder. 

## GUI

### Tkinter

We use built-in package `Tkinter` to create GUI for our system. Here is a tutorial of `Tkinter`: https://www.python-course.eu/python_tkinter.php

## Generate executable files

### Mac OS

We use `py2app` package to generate our `gui.app` file. We recommend you to use the 0.13 version, because there are some bugs in the latest version (0.14). File `setup.py` is the setup script we used for generating `gui.app`. 

For more information about `py2app`, please visit [here](http://py2app.readthedocs.io/en/latest/).

### Windows

We use `PyInstaller` to generate  `gui.exe` file for Windows users. For more information about `PyInstaller`, please visit [here](https://www.pyinstaller.org).



