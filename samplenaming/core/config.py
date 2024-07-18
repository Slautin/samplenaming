import os
import pandas as pd
from samplenaming.core.snglobal import FILE_PATH, FILE_CSV, FILE_NENTRIES
from samplenaming.core.snglobal import CSV_HEADERS


def init_files(force2init=False):
    if not os.path.isdir(FILE_PATH):
        os.makedirs(FILE_PATH)
    if force2init:
        thisinit = True
    else:
        if not os.path.isfile(os.path.join(FILE_PATH, FILE_CSV)):
            thisinit = True
        else:
            thisinit = False

    if thisinit:
        thisdf = pd.DataFrame(columns=CSV_HEADERS)
        thisdf = thisdf.rename_axis("EID")
        thisdf.to_csv(os.path.join(FILE_PATH, FILE_CSV), sep="|", index=True)
    if force2init:
        thisinit = True
    else:
        if not os.path.isfile(os.path.join(FILE_PATH,  FILE_NENTRIES)):
            thisinit = True
        else:
            thisinit = False
    if thisinit:
        nentries = 1000
        with open(os.path.join(FILE_PATH, FILE_NENTRIES), "w") as f:
            f.write(str(nentries))