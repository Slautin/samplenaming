import os
import numpy as np
import pandas as pd
from monty.io import zopen
import datetime

from samplenaming.core.snglobal import FILE_PATH, FILE_CSV
from samplenaming.core.snglobal import CSV_HEADERS, CSV_HEADERS_SHORT
from samplenaming.core.classes import SNEntry
from samplenaming.periodictable.composition import Composition


class SNSummary:
    def __init__(self):
        self.df = pd.read_csv(os.path.join(FILE_PATH, FILE_CSV), sep="|")
        self.df = self.df.set_index("SID", drop=True)
        self.nentries = len(self.df)
        self.df4query = self.df.copy(deep=True)
        self.last_access = datetime.datetime.now()

    def __str__(self):
        print("=============================================")
        thismsg = f"last access time: {self.last_access} number of entries: {self.nentries}"
        print(thismsg)
        print("=============================================")
        print(self.df.tail())
        return thismsg

    def __repr__(self):
        return self.__str__()

    def reset_df4query(self):
        self.df4query = self.df.copy(deep=True)

    def delete_by_ids(self, ids):
        for i in sorted(ids, reverse=True):
            qrstring = self.df.at[i, "QRcode"]
            qrstring = qrstring.split("_")
            foldname = qrstring[0]
            fname = qrstring[-1]
            for file in os.listdir(os.path.join(FILE_PATH, foldname)):
                if fname in file:
                    os.remove(os.path.join(FILE_PATH, foldname, file))
            self.df = self.df.drop(index=i)
        self.nentries = len(self.df)
        self.reset_df4query()

    def delete_by_qrstring(self, value):
        ys = self.df["QRcode"].to_numpy()
        ids = self.df.index.to_numpy()
        ids = np.compress(ys == value, ids)
        self.delete_by_ids(ids)

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
        thisstr = str(thisdict["SampleID"])
        for k in range(len(CSV_HEADERS)):
            key = CSV_HEADERS[k]
            thisstr += "|"+str(thisdict[key])
        if len(thisstr) > 20:
            with zopen(filename, "a") as f:
                f.write("\n".join([thisstr])+"\n")

    def add_an_entry(self, upload_files=None):
        thisentry = SNEntry.from_input(upload_files=upload_files)
        thisdict = thisentry.to_dict()
        SNSummary.to_file(thisdict)
        self.df.loc[thisdict["SampleID"]] = thisdict
        self.nentries = len(self.df)
        self.reset_df4query()

    def add_an_entry_from_id(self, thisid, upload_files=None):
        indict = self.df.loc[thisid].to_dict()
        thisentry = SNEntry.from_history(indict, upload_files=upload_files)
        thisdict = thisentry.to_dict()
        SNSummary.to_file(thisdict)
        self.df.loc[thisdict["SampleID"]] = thisdict
        self.nentries = len(self.df)
        self.reset_df4query()

    def add_an_entry_from_qrcode(self, value, upload_files=None):
        ys = self.df["QRcode"].to_numpy()
        ids = self.df.index.to_numpy()
        ids = np.compress(ys == value, ids)
        indict = self.df.iloc[ids[0]].to_dict()
        thisentry = SNEntry.from_history(indict, upload_files=upload_files)
        thisdict = thisentry.to_dict()
        SNSummary.to_file(thisdict)
        self.df.loc[thisdict["SampleID"]] = thisdict
        self.nentries = len(self.df)
        self.reset_df4query()

    def query_save(self, filename="SNquery_results.csv"):
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
        ids = self.df4query.index.to_numpy()
        return ids

    def query_by_ncompons(self, ncompons, reset_df=False):
        if reset_df:
            self.reset_df4query()
        ys = self.df4query["Elements"].to_numpy()
        inds = []
        for i in range(len(ys)):
            compstr = ys[i]
            comp = Composition(compstr)
            thisn = len(comp.elements)
            if thisn in ncompons:
                inds.append(i)
        inds = np.array(inds).astype(int)
        self.df4query = self.df4query.iloc[inds]
        ids = self.df4query.index.to_numpy()
        return ids

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
        ids = self.df4query.index.to_numpy()
        return ids

    def query_by_key_value_in(self, key, value, reset_df=False):
        if reset_df:
            self.reset_df4query()
        ys = self.df4query[key].to_numpy()
        inds = []
        for i in range(len(ys)):
            thisv = ys[i]
            if value in thisv:
                inds.append(i)
        inds = np.array(inds).astype(int)
        self.df4query = self.df4query.iloc[inds]
        ids = self.df4query.index.to_numpy()
        return ids

    def query_by_ids(self, ids):
        ids = np.array(ids, dtype=int)
        self.reset_df4query()
        self.df4query = self.df4query.loc[ids]

    def query_by_qrstring(self, value):
        self.reset_df4query()
        ys = self.df4query["QRcode"].to_numpy()
        inds = np.arange(len(ys), dtype=int)
        inds = np.compress(ys == value, inds)
        self.df4query = self.df4query.iloc[inds]
        ids = self.df4query.index.to_numpy()
        return ids
