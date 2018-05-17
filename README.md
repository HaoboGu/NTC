## Introduction 

This repository contains code for a spelling correction system for OCR errors in historical text. Our goal of this project is to build a system can automatically recognize and correct errors and generate relatively clean text for next step. 



## Requirements

This project requires python3 and NLTK. NLTK can be installed using:

```
pip install -U nltk
```

Additional NLTK data is required. You can use the following command to get all data installed: 

```
python -m nltk.downloader all
```



## Usage

You can use the following command to generate corrected text:

```
src/correct_ocr.py input_filename output_filename [gold_standard_filename]
```

Note that input file should be plain text. Other format like XML/HTML will not be accepted. 

`gold_standard_filename` is an optional argument. If the gold stanard file is specified, our system will print out word error rate (WER) calculated using gold standard file as the reference. 

