import os, sys
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
SYN_HEADERS = ["Synthesis", "SynParams"]
CHAR_HEADERS = ["Characterization", "CharParams"]
ADD_HEADERS = ["ResearchGroup", "QRcode", "Initials", "Comments"]
GENERATE_HEADERS = ["DateTime", "nFiles", "SampleFolder", "SampleName", "SampleID"]
CSV_HEADERS = COMP_HEADERS + SYN_HEADERS + CHAR_HEADERS + ADD_HEADERS + GENERATE_HEADERS
CSV_HEADERS_SHORT = ["Elements", "Composition", "Synthesis", "Characterization", "Comments", "SampleID"]

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