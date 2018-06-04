import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '../'))
import src.ngram as ng


if __name__ == "__main__":
    if 'data' in os.listdir('.'):
        data_path = './data/'
        model_path = "./model/"
    else:
        data_path = '../data/'
        model_path = "../model/"
    ng.ngrammodel(data_path, model_path, split_strategy=ng.TOKENIZER, modern_corpus=False)

