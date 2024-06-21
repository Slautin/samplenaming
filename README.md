
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

I have put several Python codes to show how to use it. The main code is located at samplenaming/core/snsummary.py. For those who are familar with Python, you can read the source code for additional functions/methods of the SNSummary object.

The firsttime.py is to generate the folder and files. Only run once after installation.

The add_an_entry.py is to add an entry to database. 
```bash
from samplenaming.core.snsummary import SNSummary

thissummary = SNSummary()

## add an entry without uploading files
from samplenaming.core.snsummary import SNSummary

thissummary = SNSummary()
SNSummary.display_entries(thissummary.df, display_style="compact")

## add an entry with uploading files
upload_files = ["upload1.txt", "upload2.in"]
thissummary.add_an_entry(upload_files=upload_files)
SNSummary.display_entries(thissummary.df, display_style="compact")


## add an entry based on the previous sample in database (from sample ID)
upload_files = None
thissid = 1002
thissummary.add_an_entry_from_id(thissid, upload_files=upload_files)
SNSummary.display_entries(thissummary.df, display_style="Full")

## add an entry based on the previous sample in database (from QRcode)
## thissummary.add_an_entry_from_qrcode(qrstring, upload_files=None)
```

The query.py is to screen entries and save the results
```bash
from samplenaming.core.snsummary import SNSummary

print("========== Original Entries ============")
thissummary = SNSummary()
SNSummary.display_entries(thissummary.df, display_style="compact")

print("========== After first screening ============")
elements = ["H"]
style = "INCLUDE" #option: "EXCLUDE"
ids = thissummary.query_by_elements(elements, style=style, reset_df=False)
thissummary.query_display(display_style="compact")

print("========== Continueous screening ============")
key = "Elements"
thisvalue = ["HO"]
ids = thissummary.query_by(key, thisvalue)
display_cols = ["Composition", "Synthesize", "Syn_params", "QRcode"]
thissummary.query_display(display_style=display_cols)

### save to file #####
filename = "SNquery_results.csv"
thissummary.query_save(filename=filename)
```
