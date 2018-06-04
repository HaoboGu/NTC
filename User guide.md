# User Guide


## Introduction 

This document contains user guide for running our program. 



## Requirements

### Windows

If you are Windows users, please download all files and you can run the program by double clicking `gui.exe`. No any other installations are required. 

### Mac OS

If you are Mac OS users, you can just download `gui.app` and run the program by double clicking the icon. However, you are required to install Python3 and NLTK package before running our program.

### Python installation

You can download Python3.6.5 [here](https://www.python.org/downloads/release/python-365/). For beginners, we recommand the offical [tutorial](https://docs.python.org/3.6/tutorial/index.html).

### NLTK installation

For Mac/Unix, NLTK can be installed using:

```
sudo pip install -U nltk
```

(Note: if `pip` doesn't work, please try `pip3` again)

`pip` is installed with python by default. If you don't have `pip` on your computer, check [https://pip.pypa.io/en/stable/installing](https://pip.pypa.io/en/stable/installing/).

For Windows, if you have already installed Python3, you can download NLTK binary file at http://pypi.python.org/pypi/nltk. Or you can install it using:

```
pip install nltk
```

Additional NLTK data is required. Before installing NLTK data, you should install certificates. 

1. Change directory to the python folder: `cd /Applications/Python 3.6/`
2. Run the command: `./Install Certificates.command`

You can use the following command to get all data installed: 

1. Open python: `python3`

2. Import nltk: `import nltk`

3. Download and install: 
```
nltk.download(‘punkt’)
nltk.download(‘average_preceptron_tagger’)
```
4. Exit python environment: `exit()`

Here is an offical tutorial of installing [NLTK](https://www.nltk.org/install.html) and its [data](https://www.nltk.org/data.html). If you have any problems, please feel free to vist. 

## Usage

We provide a executable file under the root directory. If you are a Mac user, you can just execute `gui.app` and if you are a Windows user, you can just execute `gui.exe`. 

If you are familiar with python and want to open GUI by command line, you can use the following command under the root directory of the project: 

```
python3 src/gui.py
```

If you don't want to use GUI, you can process a raw text file directly by the following command: 

```
python3 src/correct_ocr.py input_filename output_filename [gold_standard_filename]
```
`input_filename` is the file name of raw text you want to process;

`output_file` is the output file name of the corrected text, in plain text format;

`[gold_standard_filename]` is an optional argument. If the gold stanard file is specified, our system will print out word error rate (WER) calculated using gold standard file as the reference. 

Note that the input file is required to be a plain text. Other formats like XML/HTML will not be accepted.
