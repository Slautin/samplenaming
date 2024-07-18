import os
import sys
from monty.serialization import loadfn

try:
    config_vars = loadfn(os.path.join(os.path.expanduser('~'), 'samplenaming.yaml'))
except:
    sys.exit('No samplenaming.yaml file was found. Please configure the '
    ' samplenaming.yaml and put it in your home directory.')

FILE_PATH = config_vars["FILE_PATH"]
FILE_CSV = "SampleNaming.csv"
FILE_NENTRIES = "entrycounter.txt"

COMP_HEADERS = ["Elements", "Composition", "CommonName"]
TYPING_HEADERS = ["Synthesis", "SynDetails", "Characterization", "CharDetails",
                  "iUsage", "iCreate", "RadiationDetails", "ResearchGroup",  "YourName", "PaperLink", "Comments"]
GENERATE_HEADERS = ["QRString", "DateTime", "nFiles", "FileFolder", "FileHeader", "FileLinks",
                    "EntryID", "FirstSampleID", "NearestSampleID", "History"]
CSV_HEADERS = COMP_HEADERS + TYPING_HEADERS + GENERATE_HEADERS
CSV_HEADERS_SHORT = ["Elements", "Composition", "Synthesis", "Characterization", "History", "EntryID", "NearestSampleID"]
CSV_HEADERS_QUERY = ["Elements", "Composition", "Synthesis", "Characterization", "History", "EntryID",
                     "FirstSampleID", "NearestSampleID", "FileLinks"]

CSV_HEADERS_SAME = ["Elements", "Composition", "CommonName",
                    "Synthesis", "SynDetails", "Characterization", "CharDetails",
                    "RadiationDetails", "NearestSampleID"]
CSV_HEADERS_MERGE = ["ResearchGroup",  "YourName", "PaperLink", "Comments"]
CSV_HEADERS_UPDATE = ["DateTime",  "nFiles"]

Synthesis = ["Casting", "Sputter", "SolidState", "StericEntrapment", "AdditiveMan", "Computation", "Others", "Combination", "Unknown"]
Characterization = ["XRD", "SEM", "TEM", "Metallography", "MicroHardness", "MechanicalTest", "Others", "Combination", "Unknown"]

NANSTRINGS = ["NAN", "NA", "N/A", "N\A"]


def get_nentries():
    with open(os.path.join(FILE_PATH, FILE_NENTRIES), "r") as f:
        line = f.readline()
        nentries = int(line)
    return nentries


def write_nentries(nentries):
    with open(os.path.join(FILE_PATH, FILE_NENTRIES), "w") as f:
        f.write(str(nentries))