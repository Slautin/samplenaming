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

COMP_HEADERS = ["Elements", "Composition"]
SYN_HEADERS = ["Synthesis", "SynDetails"]
CHAR_HEADERS = ["Characterization", "CharDetails"]
ADD_HEADERS = ["ResearchGroup", "QRcode", "Initials", "History"]
GENERATE_HEADERS = ["DateTime", "nFiles", "SampleFolder", "SampleName", "SampleID"]
CSV_HEADERS = COMP_HEADERS + SYN_HEADERS + CHAR_HEADERS + ADD_HEADERS + GENERATE_HEADERS
CSV_HEADERS_SHORT = ["Elements", "Composition", "Synthesis", "Characterization", "History", "SampleID"]

Synthesis = ["Casting", "Sputter", "Wrought", "Deposition", "Computation", "Others", "Combination", "Unknown"]
Characterization = ["XRD", "SEM", "TEM", "Metallography", "MicroHardness", "MechanicalTest", "Others", "Combination", "Unknown"]
