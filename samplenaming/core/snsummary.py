import os
import numpy as np
import pandas as pd
from monty.io import zopen

from samplenaming.core.snglobal import FILE_PATH, FILE_CSV, ACCESS_DATETIME, CSV_HEADERS, CSV_HEADERS_SHORT
from samplenaming.core.classes import SNEntry
from samplenaming.periodictable.composition import Composition


class SNSummary:
    def __init__(self):
        self.df = pd.read_csv(os.path.join(FILE_PATH, FILE_CSV), sep="|")
        self.list_dicts = self.df.to_dict(orient='records')
        self.nentries = len(self.df)
        self.df4query = self.df.copy(deep=True)
        inds = np.arange(len(self.df), dtype=int)
        self.df4query["tmpindex"] = inds

    def reset_df4query(self):
        self.df4query = self.df.copy(deep=True)
        inds = np.arange(len(self.df), dtype=int)
        self.df4query["tmpindex"] = inds

    @staticmethod
    def display_entries(thisdf, display_style="Compact"):
        if isinstance(display_style, list):
            display_cols = []
            for key in display_style:
                if key in CSV_HEADERS:
                    display_cols.append(key)
        else:
            if display_style.upper() == "ALL" or display_style.upper() == "FULL":
                display_cols = CSV_HEADERS[0:len(CSV_HEADERS)]
            else:
                display_cols = CSV_HEADERS_SHORT[0:len(CSV_HEADERS_SHORT)]
        print(thisdf[display_cols])

    @staticmethod
    def to_file(thisdict):
        filename = os.path.join(FILE_PATH, FILE_CSV)
        thisstr = ""
        for k in range(len(CSV_HEADERS)):
            key = CSV_HEADERS[k]
            if k == 0:
                thisstr = str(thisdict[key])
            else:
                thisstr += "|"+str(thisdict[key])
        if len(thisstr) > 20:
            with zopen(filename, "a") as f:
                f.write("\n".join([thisstr])+"\n")

    def add_an_entry(self, upload_files=None):
        thisentry = SNEntry.from_input(upload_files=upload_files)
        thisdict = thisentry.to_dict()
        SNSummary.to_file(thisdict)
        self.df.loc[len(self.df)] = thisdict
        self.list_dicts.append(thisdict)
        self.nentries = len(self.df)
        self.reset_df4query()

    def delete_by_ids(self, inds):
        inds = list(inds)
        inds = list(set(inds))
        for i in sorted(inds, reverse=True):
            qrstring = self.list_dicts[i]["QRcode"]
            qrstring = qrstring.split("_")
            foldname = qrstring[0]
            fname = qrstring[-1]
            for file in os.listdir(os.path.join(FILE_PATH, foldname)):
                if fname in file:
                    os.remove(os.path.join(FILE_PATH, foldname, file))
            del self.list_dicts[i]
        self.nentries = len(self.list_dicts)
        self.df = pd.DataFrame(self.list_dicts, columns=CSV_HEADERS)
        self.df.to_csv(os.path.join(FILE_PATH, FILE_CSV), sep="|", index=False)
        self.reset_df4query()

    def delete_by_qrstring(self, value):
        ys = self.df["QRcode"].to_numpy()
        inds = np.arange(len(ys), dtype=int)
        inds = np.compress(ys == value, inds)
        self.delete_by_ids(inds)

    def query_save(self, filename="SNquery_results.csv"):
        SNSummary.display_entries(self.df4query, display_style="Compact")
        self.df4query.to_csv(filename, sep="|", index=False)

    def query_display(self, display_style="Compact"):
        SNSummary.display_entries(self.df4query, display_style=display_style)

    def query_by_elements(self, elements, style="INCLUDE", reset_df=False):
        if reset_df:
            self.reset_df4query()
        ys = self.df4query["Elements"].to_numpy()
        inds = np.arange(len(ys), dtype=int)
        bads = []
        for i in range(len(ys)):
            compstr = ys[i]
            isvalid = True
            for sym in elements:
                if sym in compstr:
                    if style[0:3].upper() == "INC":
                        pass
                    else:
                        isvalid = False
                        break
                else:
                    if style[0:3].upper() == "INC":
                        isvalid = False
                        break
                    else:
                        pass
            if not isvalid:
                bads.append(i)
        bads = np.array(bads).astype(int)
        inds = np.delete(inds, bads)
        self.df4query = self.df4query.iloc[inds]
        inds = self.df4query["tmpindex"].to_numpy()
        return inds

    def query_by_ncompons(self, ncompons, reset_df=False):
        if reset_df:
            self.reset_df4query()
        ys = self.df4query["Elements"].to_numpy()
        inds = np.arange(len(ys), dtype=int)
        bads = []
        for i in range(len(ys)):
            compstr = ys[i]
            comp = Composition(compstr)
            thisn = len(comp.elements)
            isvalid = True
            if thisn in ncompons:
                pass
            else:
                isvalid = False
            if not isvalid:
                bads.append(i)
        bads = np.array(bads).astype(int)
        inds = np.delete(inds, bads)
        self.df4query = self.df4query.iloc[inds]
        inds = self.df4query["tmpindex"].to_numpy()
        return inds

    def query_by(self, key, values, reset_df=False):
        if reset_df:
            self.reset_df4query()
        if isinstance(values, str) or isinstance(values, float) or isinstance(values, int):
            values = [values]
        if not isinstance(values, list):
            raise ValueError("values must be a list!")
        inds = np.array([], dtype=int)
        for value in values:
            thisdf = self.df4query.copy(deep=True)
            if key in CSV_HEADERS:
                ys = thisdf[key].to_numpy()
                linds = np.arange(len(ys), dtype=int)
                linds = np.compress(ys == value, linds)
                inds = np.append(inds, linds)
        self.df4query = self.df4query.iloc[inds]
        inds = self.df4query["tmpindex"].to_numpy()
        return inds

    def query_by_ids(self, inds):
        self.reset_df4query()
        inds = np.array(inds)
        self.df4query = self.df4query.iloc[inds]
        return inds

    def query_by_qrstring(self, value):
        self.reset_df4query()
        ys = self.df4query["QRcode"].to_numpy()
        inds = np.arange(len(ys), dtype=int)
        inds = np.compress(ys == value, inds)
        self.df4query = self.df4query.iloc[inds]
        inds = self.df4query["tmpindex"].to_numpy()
        return inds

    def __str__(self):
        print("=============================================")
        thismsg = f"last access time: {ACCESS_DATETIME} number of entries: {self.nentries}"
        print(thismsg)
        print("=============================================")
        print(self.df.tail())
        return thismsg

    def __repr__(self):
        return self.__str__()
