
# Sample naming for CAMM_MSERC at University of Tennessee, Knoxville

A Python code package for sample naming.


## Installation

Install samplenaming with python. 
Step 1: clone the code to your local computer, and then run "python setup.py install" in the samplenaming folder.
```bash
  git clone git@github.com:TaoLiang120/samplenaming.git
  cd samplenaming
  python setup.py install
```
Step 2: edit and copy samplenaming.yaml to your root directory. You can use any text editor to change samplenaming.yaml. Below,  I use "vi" command in OS or Linux systems as an example.
```bash
  vi samplenaming.yaml 
  cp samplenaming.yaml ~
```
If you encounter any problem with unknown modules, just run "pip install modulename".   
## Tao Liang  tliang7@utk.edu

- [@TaoLiang120](https://github.com/TaoLiang120/samplenaming)


## Usage/Examples

I have put several lines of Python codes to show how to use it. The main code is located at samplenaming/core/snsummary.py. For those who are familar with Python, you can read the source code for additional functions/methods of the SNSummary object.

```bash
from samplenaming.core.snglobal import CSV_HEADERS, CSV_HEADERS_SHORT
print(CSV_HEADERS)
print(CSV_HEADERS_SHORT)

from samplenaming.core.snsummary import SNSummary

thissummary = SNSummary()
SNSummary.display_entries(thissummary.df, display_style="compact")
thissummary.add_an_entry()
SNSummary.display_entries(thissummary.df, display_style="Full")

elements = ["H"]
style = "INCLUDE" #option: "EXCLUDE"
ids = thissummary.query_by_elements(elements, style=style, reset_df=False)
print("===")

key = "Elements"
thisvalue = "HO"
ids = thissummary.query_by(key, thisvalue)
print("===")

display_cols = ["Composition", "Synthesize", "Syn_params", "QRcode"]
thissummary.query_display(display_style=display_cols)
print("===")

filename = "tmp.csv"
thissummary.query_save(filename="SNquery_results.csv")
```

