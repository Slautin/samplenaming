import os, sys
from monty.serialization import loadfn

try:
    config_vars = loadfn(os.path.join(os.path.expanduser('~'), 'samplenaming.yaml'))
except:
    sys.exit('No samplenaming.yaml file was found. Please configure the '
    ' samplenaming.yaml and put it in your home directory.')

FILE_PATH = config_vars["FILE_PATH"]
FILE_CSV = "SampleNaming.csv"
IDBASE = 100000

OBJECT_HEADERS = ["Elements", "Composition", "Synthesize", "Characterization", "ResearchGroup", "QRcode"]
CUSTOM_HEADERS = ["Initials", "Comments", "nFiles"]
GENERATE_HEADERS  =  ["SampleFolder", "SampleID", "SampleName"]
CSV_HEADERS = OBJECT_HEADERS+CUSTOM_HEADERS+GENERATE_HEADERS

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
    "Xu,Haixuan": {
        "ID": "A"
    },
    "Unknown": {
        "ID": "A"
    },
}

Synthesize = {
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