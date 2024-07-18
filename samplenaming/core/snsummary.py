import os
import numpy as np
import pandas as pd
from monty.io import zopen
import datetime
import shutil

from samplenaming.core.snglobal import FILE_PATH, FILE_CSV
from samplenaming.core.snglobal import CSV_HEADERS, CSV_HEADERS_SHORT, CSV_HEADERS_QUERY
from samplenaming.core.snglobal import CSV_HEADERS_SAME, CSV_HEADERS_MERGE, CSV_HEADERS_UPDATE, NANSTRINGS
from samplenaming.core.classes import SNEntry
from samplenaming.periodictable.composition import Composition


def ismerge_twodicts(firstdict, seconddict):
    ismerge = True
    for key in CSV_HEADERS_SAME:
        if firstdict[key] != seconddict[key]:
            ismerge = False
            break
    return ismerge


def merge_twodicts(firstdict, seconddict):
    for key in CSV_HEADERS_MERGE:
        if len(firstdict[key]) == 0 or firstdict[key].upper() in NANSTRINGS:
            firstdict[key] = seconddict[key]
        else:
            firstdict[key] += "," + str(seconddict[key])
    for key in CSV_HEADERS_UPDATE:
        if key == "DateTime":
            firstdict[key] = str(datetime.datetime.now())
        elif key == "nFiles":
            foldname = seconddict["FileFolder"]
            oldfheader = seconddict["FileHeader"]
            fheader = (firstdict["CommonName"] + "_"
                       + firstdict["Synthesis"] + "_" + firstdict["Characterization"] +
                        "_EID" + str(firstdict["EntryID"]))
            nfiles = firstdict[key]
            filelinks = firstdict["FileLinks"]
            files = os.listdir(os.path.join(FILE_PATH, foldname))
            for f in files:
                if oldfheader in f:
                    app = f.split(".")
                    app = app[-1]
                    tf = fheader + "_F" + str(nfiles + 1)
                    tf = tf + "." + app
                    filelinks += "FileLink" + str(nfiles + 1) + " "
                    thislink = os.path.join(FILE_PATH, foldname, tf)
                    shutil.copy(os.path.join(FILE_PATH, foldname, f), os.path.join(FILE_PATH, foldname, tf))
                    nfiles += 1
            firstdict[key] = nfiles
            firstdict["FileLinks"] = filelinks
    return firstdict


class SNSummary:
    def __init__(self):
        self.df = pd.read_csv(os.path.join(FILE_PATH, FILE_CSV), sep="|")
        self.df = self.df.set_index("EID", drop=True)
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
        ids = list(ids)
        for i in sorted(ids, reverse=True):
            qrstring = self.df.at[i, "QRString"]
            qrstring = qrstring.split("_")
            foldname = qrstring[0]
            fname = qrstring[-1]
            for file in os.listdir(os.path.join(FILE_PATH, foldname)):
                if fname in file:
                    os.remove(os.path.join(FILE_PATH, foldname, file))
            self.df = self.df.drop(index=i)
        self.df.to_csv(os.path.join(FILE_PATH, FILE_CSV), sep="|", index=True)
        self.nentries = len(self.df)
        self.reset_df4query()

    def delete_by_qrstring(self, value):
        ys = self.df["QRString"].to_numpy()
        ids = self.df.index.to_numpy()
        ids = np.compress(ys == value, ids)
        self.delete_by_ids(ids)

    def merge_entries(self):
        self.df = self.df.sort_index()
        avids = self.df.index.to_numpy()
        todel = []
        hs = self.df["History"].to_numpy()
        for i in range(self.nentries-1, -1, -1):
            thish = hs[i]
            thish = thish.split(",")
            thisids = []
            for ii in range(len(thish)):
                try:
                    thisid = int(thish[ii])
                    thisids.append(thisid)
                except:
                    pass
            if len(thisids) >= 1 and thisids[-1] in avids:
                firstdict = self.df.loc[thisids[-2]].to_dict()
                seconddict = self.df.loc[thisids[-1]].to_dict()
                ismerge = ismerge_twodicts(firstdict, seconddict)
                if ismerge:
                    firstdict = merge_twodicts(firstdict, seconddict)
                    self.df.loc[thisids[-2]] = firstdict
                    todel.append(i)
                else:
                    avids = np.delete(avids, np.where(avids == thisids[-2]))
            else:
                pass
            avids = np.delete(avids, np.where(avids == thisids[-1]))
        self.delete_by_ids(todel)

    def edit_an_entry(self, thisid, indict):
        thisdict = self.df.loc[thisid].to_dict()
        for key in indict:
            if key in CSV_HEADERS:
                thisdict[key] = indict[key]
        self.df.loc[thisid] = thisdict
        self.df.to_csv(os.path.join(FILE_PATH, FILE_CSV), sep="|", index=True)
        self.nentries = len(self.df)
        self.reset_df4query()

    @staticmethod
    def display_entries(thisdf, display_style="Compact"):
        display_cols = []
        if isinstance(display_style, list):
            all_cols = thisdf.columns.to_list()
            for key in display_style:
                if key in all_cols:
                    display_cols.append(key)
        else:
            if display_style.upper() == "ALL" or display_style.upper() == "FULL":
                display_cols = thisdf.columns.to_list()
            elif display_style.upper() == "QUERY" or display_style.upper() == "Screen":
                display_cols = CSV_HEADERS_QUERY[0:len(CSV_HEADERS_QUERY)]
            else:
                display_cols = CSV_HEADERS_SHORT[0:len(CSV_HEADERS_SHORT)]
        print(thisdf[display_cols])

    @staticmethod
    def to_file(thisdict):
        filename = os.path.join(FILE_PATH, FILE_CSV)
        thisstr = str(thisdict["EntryID"])
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
        self.df.loc[thisdict["EntryID"]] = thisdict
        self.nentries = len(self.df)
        self.reset_df4query()

    def add_an_entry_from_id(self, thisid, upload_files=None):
        try:
            indict = self.df.loc[thisid].to_dict()
        except:
            errormsg = f"The entry ID of {thisid} is not existed in database."
            raise ValueError(errormsg)
        thisentry = SNEntry.from_history(indict, upload_files=upload_files)
        thisdict = thisentry.to_dict()
        SNSummary.to_file(thisdict)
        self.df.loc[thisdict["EntryID"]] = thisdict
        self.nentries = len(self.df)
        self.reset_df4query()

    def add_an_entry_from_qrstring(self, value, upload_files=None):
        ys = self.df["QRString"].to_numpy()
        ids = self.df.index.to_numpy()
        ids = np.compress(ys == value, ids)
        if len(ids) == 0:
            errormsg = f"The QRstring of {value} is not existed in database."
            raise ValueError(errormsg)
        indict = self.df.iloc[ids[0]].to_dict()
        thisentry = SNEntry.from_history(indict, upload_files=upload_files)
        thisdict = thisentry.to_dict()
        SNSummary.to_file(thisdict)
        self.df.loc[thisdict["EntryID"]] = thisdict
        self.nentries = len(self.df)
        self.reset_df4query()

    def query_save(self, filename="SNquery_results.csv"):
        self.df4query.to_csv(filename, sep="|", index=False)

    def query_display(self, display_style="Query"):
        SNSummary.display_entries(self.df4query, display_style=display_style)

    def query_by_elements(self, elements, style="INCLUDE", reset_df=False):
        if reset_df:
            self.reset_df4query()
        nele = len(elements)
        ys = self.df4query["Elements"].to_numpy()
        inds = np.arange(len(ys), dtype=int)
        bads = []
        for i in range(len(ys)):
            compstr = ys[i]
            isvalid = True
            comp = Composition(compstr)
            thiseles = []
            for ele in comp.elements:
                thiseles.append(ele.symbol)
            if style[0:3].upper() == "EXA":
                if len(thiseles) != nele:
                    isvalid = False
            if isvalid:
                for sym in elements:
                    if sym in thiseles:
                        if style[0:3].upper() == "EXC":
                            isvalid = False
                            break
                    else:
                        if style[0:3].upper() == "INC" or style[0:3].upper() == "EXA":
                            isvalid = False
                            break

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
            thisv = str(ys[i])
            if str(value) in thisv:
                inds.append(i)
        inds = np.array(inds).astype(int)
        self.df4query = self.df4query.iloc[inds]
        ids = self.df4query.index.to_numpy()
        return ids

    def query_by_ids(self, ids):
        ids = np.array(ids, dtype=int)
        self.reset_df4query()
        self.df4query = self.df4query.loc[ids]
        return ids

    def query_by_qrstring(self, value):
        self.reset_df4query()
        ys = self.df4query["QRString"].to_numpy()
        inds = np.arange(len(ys), dtype=int)
        inds = np.compress(ys == value, inds)
        self.df4query = self.df4query.iloc[inds]
        ids = self.df4query.index.to_numpy()
        return ids
