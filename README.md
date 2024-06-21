
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
```
in addition to add_an_entry_from_id, you add an entry based on previous QRcode in database by add_an_entry_from_qrcode(qrstring, upload_files=None).


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

the reset_df in functions above is used to turn on/off continueous screening. If False, continueous screening, else reset to dataframe to original dataframe. In addition to query_by_elements() and query_by() functions, list below are available querying functions with return of sampleids in SNSummary:
1. query_by_ncompons(ncompons, reset_df=False); ncompons: list of number of elements, eg. [3, 4, 5]
2. query_by_key_value_in(key, value, reset_df=False), key: keyword in SNSummary, value: value string is part of key value of database 
3. query_by_qrstring(value), value: qrstring
The query_by_ids(sids), where sids are a list of sample IDs, is querying your results based on sids. No returns. 
