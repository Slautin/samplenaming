import os, sys
from monty.serialization import loadfn
import pandas as pd
import datetime

try:
    config_vars = loadfn(os.path.join(os.path.expanduser('~'), 'samplenaming.yaml'))
except:
    sys.exit('No samplenaming.yaml file was found. Please configure the '
    ' samplenaming.yaml and put it in your home directory.')

FILE_PATH = config_vars["FILE_PATH"]
FILE_CSV = "SampleNaming.csv"

COMP_HEADERS = ["Elements", "Composition"]
SYN_HEADERS = ["Synthesis", "SynID", "SynParams"]
CHAR_HEADERS = ["Characterization", "CharID", "CharParams"]
ADD_HEADERS = ["ResearchGroup", "GroupID", "QRcode", "Initials", "Comments"]
GENERATE_HEADERS = ["SampleFolder", "SampleName", "nFiles"]
CSV_HEADERS = COMP_HEADERS + SYN_HEADERS + CHAR_HEADERS + ADD_HEADERS + GENERATE_HEADERS
CSV_HEADERS_SHORT = ["Elements", "Composition", "Synthesis", "Characterization", "QRcode", "nFiles"]
ACCESS_DATETIME = datetime.datetime.now()

if not os.path.isfile(os.path.join(FILE_PATH, FILE_CSV)):
    thisdf = pd.DataFrame(columns=CSV_HEADERS)
    thisdf.to_csv(os.path.join(FILE_PATH, FILE_CSV), sep="|", index=False)

Synthesis = {
    "Casting": {
        "ID": "A",
        "Cooling": "Air",
        "AnnealTemperature": 500.0,
        "AnnealTime": 180.0,
    },
    "Sputter": {
        "ID": "B",
        "Substrate": "Si",
        "Temperature": 1800.0,
    },
    "Computation": {
        "ID": "C",
        "Method": "CalPHAD",
    },
    "Unknown": {
        "ID": "D",
    },
}

Characterization = {
    "XRD": {
        "ID": "A",
    },
    "SEM": {
        "ID": "B",
        "Temperature": 1800.0,
    },
    "TEM": {
        "ID": "C",
        "Temperature": 1800.0,
    },
    "MicroHardness": {
        "ID": "D",
        "Substrate": "Si",
        "Temperature": 1800.0,
    },
    "Tensile_Compressive": {
        "ID": "E",
        "Method": "Tensile",
        "StrainRate": 0.0001,
        "Temperature": 300.0,
    },
    "Unknown": {
        "ID": "E",
    },
}

ResearchGroup = {
    "Haixuan_Xu": {
        "ID": "A"
    },
    "Unknown": {
        "ID": "A"
    },
}

