# NTC: A Spelling Correction System for OCR Errors in Historical Text


## Introduction 

This repository contains code for a spelling correction system for OCR errors in historical text. Our goal of this project is to build a system can automatically recognize and correct errors and generate relatively clean text for next step. 



## Requirements

### Windows

If you are Windows users, you can run the program by double clicking gui.exe. If you have basic knowledge of Python and command line, and want the program to run faster, we recommend you to download Python3 and run the gui.py under ./src/ derectory. 

### Mac OS

If you are Mac OS users, you are required to install Python3 and NLTK package before running our program.

### Python installation

You can download Python3.6.5 [here](https://www.python.org/downloads/release/python-365/). For beginners, we recommand the offical [tutorial](https://docs.python.org/3.6/tutorial/index.html).

### NLTK installation

For Mac/Unix, NLTK can be installed using:

```
sudo pip install -U nltk
```

(Notes: if 'pip' doesn't work, please try 'pip3' again)

`pip` is installed with python by default. If you don't have `pip` on your computer, check [https://pip.pypa.io/en/stable/installing](https://pip.pypa.io/en/stable/installing/).

For windows, if you have already installed Python3, you can download NLTK binary file at http://pypi.python.org/pypi/nltk.

Additional NLTK data is required. Before installing NLTK data, you should install certificates. 

1. Change directory to the python folder: `cd /Applications/Python 3.6/`
2. Run the command: `./Install Certificates.command`

You can use the following command to get all data installed: 

1. Open python: `python3`

2. Import nltk: `import nltk`

3. Download: `nltk.download()`

4. Exit python environment: `exit()`

   

## Usage

We provide a executable file in the root directory. If you are a Mac user, you can just execute `gui` file in root directory to run our system. 

For windows users and Mac/Linux users who want to open GUI from command line, you can use the following command in the root directory of the project: 

```
python3 src/gui.py
```

We also provide a file-reader in our system:

```
python3 src/correct_ocr.py input_filename output_filename [gold_standard_filename]
```

Note that input file should be plain text. Other format like XML/HTML will not be accepted. 

`gold_standard_filename` is an optional argument. If the gold stanard file is specified, our system will print out word error rate (WER) calculated using gold standard file as the reference. 

