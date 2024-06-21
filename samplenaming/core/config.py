import os
import pandas as pd
from samplenaming.core.snglobal import FILE_PATH, FILE_CSV, FILE_NENTRIES
from samplenaming.core.snglobal import CSV_HEADERS


def init_files():
    if not os.path.isdir(FILE_PATH):
        os.makedirs(FILE_PATH)

    if not os.path.isfile(os.path.join(FILE_PATH, FILE_CSV)):
        thisdf = pd.DataFrame(columns=CSV_HEADERS)
        thisdf = thisdf.rename_axis("SID")
        thisdf.to_csv(os.path.join(FILE_PATH, FILE_CSV), sep="|", index=True)

    if not os.path.isfile(os.path.join(FILE_PATH,  FILE_NENTRIES)):
        nentries = 1000
        with open(os.path.join(FILE_PATH, FILE_NENTRIES), "w") as f:
            f.write(str(nentries))


def get_nentries():
    with open(os.path.join(FILE_PATH, FILE_NENTRIES), "r") as f:
        line = f.readline()
        nentries = int(line)
    return nentries


def write_nentries(nentries):
    with open(os.path.join(FILE_PATH, FILE_NENTRIES), "w") as f:
        f.write(str(nentries))
