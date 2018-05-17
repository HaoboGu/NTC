import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '../'))
import src.file_io as reader
import src.evaluation as evaluation
import src.ntc as ntc
import src.ngram as ng
import re

if __name__ == "__main__":
    use_local_file = False
    if use_local_file:
        if 'output' in os.listdir('.'):
            data_path = './data/'
            output_path = "./output/"
            model_path = "./model/"
        else:
            data_path = '../data/'
            output_path = "../output/"
            model_path = "../model/"
        raw_text_file = "OCR_text/newberry-mary-b-some-further-accounts-of-the-nile-1912-1913/NMB_2.txt"
        gold_text_file = "gold_standard/newberry-mary-b-some-further-accounts-of-the-nile-1912-1913/ESF_2.txt"
        input_filename = data_path + raw_text_file
        output_filename = output_path + "corrected_text.txt"
        gold_filename = data_path + gold_text_file
    else:
        if len(sys.argv) == 3:
            input_filename = sys.argv[1]
            output_filename = sys.argv[2]
            model_path = "./model/"
        elif len(sys.argv) == 4:
            input_filename = sys.argv[1]
            output_filename = sys.argv[2]
            gold_filename = sys.argv[3]
            model_path = "./model/"
        else:
            print("Please specify input and output filenames")
            exit(0)

    all_raw_text_files, all_gold_standard_files = reader.get_all_evaluation_files()
    possible_name_entity_dict = ng.get_possible_NE_list([input_filename], split_strategy=ng.TOKENIZER)
    # Read data
    data = reader.read_file(input_filename)
    data = reader.clean_empty_line(data)

    # Rule-based system
    print('Rule-based ...')
    rbm = ntc.RuleBasedModel('ruleset')
    result = []
    for line in data:
        result.append(rbm.process(line))

    # Statistical system
    print("Statistical ...")
    # ng.ngrammodel(data_path, model_path, split_strategy=ng.TOKENIZER, modern_corpus=True)
    statistic_model = ng.read_ngram_model(model_path, split_strategy=ng.TOKENIZER,
                                          topN=50, delta=0.1, threshold=1.7, NE_list=possible_name_entity_dict)
    new_result = []

    for line in result:
        if not re.match("\\s+", line):
            new_line = ng.modify_line(statistic_model, line)
            new_result.append(new_line)

    # Write result
    print('Writing result ...')
    # reader.write_file(result, output_path+'corrected_text1')
    # reader.write_file(new_result, output_path+'corrected_text2')
    reader.write_file(new_result, output_filename)

    # Evaluation
    if len(sys.argv) == 4 or use_local_file is True:
        print('Evaluation ...')
        result = reader.lines2string(result)
        new_result = reader.lines2string(new_result)
        data = reader.lines2string(data)
        gold = reader.read_file(gold_filename)
        gold = reader.clean_empty_line(gold)
        gold = reader.lines2string(gold)

        print('WER in raw text:', evaluation.evaluate(data, gold))
        print('WER after rule-based system:', evaluation.evaluate(result, gold))
        print('WER after rule-based and statistical system:', evaluation.evaluate(new_result, gold))


