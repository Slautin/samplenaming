import os
import qrcode
import shutil
import numpy as np
#import time
import datetime
from samplenaming.core.snglobal import Synthesis, Characterization
from samplenaming.core.snglobal import FILE_PATH, CSV_HEADERS, NANSTRINGS
from samplenaming.core.snglobal import get_nentries, write_nentries
from samplenaming.periodictable.composition import Composition


def input2string(instring, to_empty=False):
    instring = str(instring)
    if instring is None:
        instring = "nan"
    elif len(instring) == 0:
        instring = "nan"
    instring = instring.strip()
    instring = instring.replace("|", "")
    if instring.upper() in NANSTRINGS:
        instring = "nan"
    if to_empty: instring = instring.replace("nan", "")
    return instring


def get_bool_input():
    thisbool = input("Want to modify (Y for yes and N for no)?")
    thisbool = input2string(thisbool, to_empty=False)
    if thisbool[0].upper() == "Y":
        thisbool = True
    else:
        thisbool = False
    return thisbool


def get_comfirm_bool():
    thisbool = input("Please confirm your input (Y for yes and N for no)?")
    thisbool = input2string(thisbool, to_empty=False)
    if thisbool[0].upper() == "Y":
        thisbool = True
    else:
        thisbool = False
    return thisbool


def merge_two_strings(old, new, thres=0):
    old = str(old)
    new = str(new)
    if len(new) <= thres:
        new = ""
    if len(old) == 0 or old.upper() == "NAN":
        out = new
    else:
        if len(new) == 0 or new.upper() == "NAN":
            out = old
        else:
            out = old + "," + new
    return out

class PrettyFormula:
    def __init__(self, compstr, significant_figure=6):
        self.compstr = compstr
        self.significant_figure = significant_figure
        self.multiplier = np.power(10.0, self.significant_figure - 1)
        self.pretty_formula = self.get_pretty_formula()
    @staticmethod
    def extract_paratheses(s):
        matches = []
        start = 0
        end = 0
        while True:
            relative_s = s[start:].find("(")
            relative_e = s[end:].find(")")
            if relative_s == -1 or relative_e == -1:
                break
            matches.append(s[start + relative_s + 1:end + relative_e])
            start += 1 + relative_s
            end += 1 + relative_e
        return matches

    def compstr2frac_formula(self, instr):
        comp = Composition(instr)
        newstr = ""
        for iele in range(len(comp.elements)):
            el = comp.elements[iele]
            sym = el.symbol
            frac = comp.get_atomic_fraction(el)
            frac = round(frac, self.significant_figure)
            newstr += sym + str(frac)
        return newstr
    def normalize_composition(self):
        matches = PrettyFormula.extract_paratheses(self.compstr)
        if len(matches) == 0:
            outstr = PrettyFormula.compstr2frac_formula(self.compstr)
        else:
            outstr = self.compstr
            for i in range(len(matches)):
                c = matches[i]
                newc = PrettyFormula.compstr2frac_formula(c)
                outstr = outstr.replace(c, newc)
        return outstr
    def get_pretty_formula(self):
        outstr = self.normalize_composition()
        comp = Composition(outstr)
        newstr = ""
        for iele in range(len(comp.elements)):
            el = comp.elements[iele]
            sym = el.symbol
            pct = comp.get_atomic_fraction(el)
            pct = int(pct)
            newstr += sym + str(pct)
        comp = Composition(newstr)
        pretty_formula = comp.reduced_formula
        return pretty_formula

    def __str__(self):
        return f"The input compostionstr: {self.compstr} pretty_formula: {self.pretty_formula}."

    def __repr__(self):
        return self.__str__()

class SNComposition:
    def __init__(self, compstr, commonname=None):
        compstr = input2string(compstr, to_empty=False)
        thisPF = PrettyFormula(compstr)
        self.compstr = thisPF.pretty_formula
        comp = Composition(self.compstr)
        self.elementstr = ""
        for el in comp.elements:
            self.elementstr += el.symbol
        commonname = input2string(commonname, to_empty=False)
        if commonname == "nan":
            commonname = self.compstr
        self.commonname = commonname

    @classmethod
    def from_input(cls):
        compstr = input("Type composition (eg: H2O): ")
        compstr = input2string(compstr)
        print(f"Your composition is {compstr}.")
        thisbool = get_comfirm_bool()
        while not thisbool:
            compstr = input("Type composition (eg: H2O): ")
            compstr = input2string(compstr)
            print(f"Your composition is {compstr}.")
            thisbool = get_comfirm_bool()
        commonname = input("Type common name (eg: TTHZ): ")
        thisobj = cls(compstr, commonname=commonname)
        return thisobj

    @classmethod
    def from_history(cls, compstr, commonname):
        print("The existing composition is " + compstr + " and common name is " + commonname + ".")
        print("They are features passed from the history. You can NOT change them!")
        thisobj = cls(compstr, commonname=commonname)
        return thisobj

    def __str__(self):
        return f"The elementstr: {self.elementstr} compstr: {self.compstr}."

    def __repr__(self):
        return self.__str__()


class SNSynthesis:
    def __init__(self, method, details):
        self.method = method
        if self.method == "Unknown":
            details = "nan"
        self.details = input2string(details, to_empty=False)

    @classmethod
    def from_input(cls):
        print("List of synthesis methods: ")
        for i in range(len(Synthesis)):
            print(f"{i + 1} -- {Synthesis[i]}")

        instr = input("Select method (eg: 1): ")
        instr = input2string(instr, to_empty=False)
        while not instr[0].isdigit():
            instr = input("Select method (eg: 1): ")
            instr = input2string(instr, to_empty=False)
        try:
            method = Synthesis[int(instr[0]) - 1]
        except:
            method = "Unknown"
        if method == "Unknown":
            details = "nan"
        else:
            details = input("Type details of " + method + ": ")
        thisobj = cls(method, details)
        return thisobj

    @classmethod
    def from_history(cls, method, details):
        print("The existing synthesis method is " + method + "and synthesis details are " + details + ".")
        print(f"They are features passed from the history. You can NOT change them!")
        thisobj = cls(method, details)
        return thisobj

    def __str__(self):
        return f"Synthesis method: {self.method} details: {self.details}."

    def __repr__(self):
        return self.__str__()


class SNCharaterization:
    def __init__(self, method, details):
        self.method = method
        if self.method == "Unknown":
            details = "nan"
        self.details = input2string(details)

    @classmethod
    def from_input(cls):
        print("List of characterization methods: ")
        for i in range(len(Characterization)):
            print(f"{i + 1} -- {Characterization[i]}")

        instr = input("Select method (eg: 1): ")
        instr = input2string(instr)
        while not instr[0].isdigit():
            instr = input("Select method (eg: 1): ")
            instr = input2string(instr)
        try:
            method = Characterization[int(instr[0]) - 1]
        except:
            method = "Unknown"

        if method == "Unknown":
            details = "nan"
        else:
            details = input("Type details of " + method + ": ")
        thisobj = cls(method, details)
        return thisobj

    @classmethod
    def from_history(cls, method, details):
        methodin = method
        print("The existing characterization method is " + method + ".")
        thisbool = get_bool_input()
        if thisbool:
            print("List of characterization methods: ")
            for i in range(len(Characterization)):
                print(f"{i + 1} -- {Characterization[i]}")

            instr = input("Select method (eg: 1): ")
            instr = input2string(instr)
            while not instr[0].isdigit():
                instr = input("Select method (eg: 1): ")
                instr = input2string(instr)
            try:
                method = Characterization[int(instr[0]) - 1]
            except:
                method = "Unknown"

        if method == "Unknown":
            details = "nan"
        else:
            if methodin == method:
                print("The existing details for " + method + " is " + details + ".")
                thisbool = get_bool_input()
                if thisbool:
                    details = input("Type details of " + method + ": ")
            else:
                details = input("Type details of " + method + ": ")
        thisobj = cls(method, details)
        return thisobj

    def __str__(self):
        return f"Characterization method: {self.method} details: {self.details}."

    def __repr__(self):
        return self.__str__()

class SampleIntegrity:
    def __init__(self, iusage, icreate):
        self.iusage = iusage
        self.icreate = icreate

    @classmethod
    def from_input(cls):
        thisobj = cls(0, 1)
        return thisobj

    @classmethod
    def from_history(cls):
        instr = input("Select usage of the sample (0 for all, 1 for part of sample): ")
        instr = input2string(instr)
        while not instr[0].isdigit():
            instr = input("Select usage of the sample (0 for all, 1 for part of sample): ")
            instr = input2string(instr)
        iusage = int(instr[0])
        if iusage != 1:
            iusage = 0

        if iusage == 0:
            outstring = "Create a new sample?"
            outstring += ("\n" +
                          "If the microstructure of the sample has been changed after this entry,"
                          " for example exposing it to irradiation, your answer would be Yes."
                          + "\n" + "Otherwise, your answer would be No")
            print(outstring)
            instr = input("Create a new sample? (0 for No, 1 for Yes): ")
            instr = input2string(instr)
            while not instr[0].isdigit():
                instr = input("Create a new sample? (0 for No, 1 for Yes): ")
                instr = input2string(instr)
            icreate = int(instr[0])
            if icreate != 1:
                icreate = 0
        else:
            outstring = "Create a new sample?"
            outstring += ("\n" +
                          "If you use part of a sample and this part of the sample is still trackable after usage,"
                          " your answer would be Yes."
                          + "\n" + "Otherwise, your answer would be No")
            print(outstring)
            instr = input("Create a new sample? (0 for No, 1 for Yes): ")
            instr = input2string(instr)
            while not instr[0].isdigit():
                instr = input("Create a new sample? (0 for No, 1 for Yes): ")
                instr = input2string(instr)
            icreate = int(instr[0])
            if icreate != 1:
                icreate = 0
        thisobj = cls(iusage, icreate)
        return thisobj

    def __str__(self):
        return f"Sample integrity. iusage: {self.iusage} icreate: {self.icreate}."

    def __repr__(self):
        return self.__str__()


class SNRadiation:
    def __init__(self, details, icreate):
        self.details = input2string(details, to_empty=True)
        if len(self.details) <= 5:
            self.details = ""
        self.icreate = icreate

    @classmethod
    def from_input(cls):
        print("A valid radiation input has be longer than 5 characters. Otherwise, no radiation.")
        radiation = input("Type radiation details: ")
        thisobj = cls(radiation, 1)
        return thisobj

    @classmethod
    def from_history(cls, previous_radiation):
        print("The existing radiation details are " + previous_radiation + ".")
        print("The following input is ADDITIONAL radiation that the sample exposed to.")
        print("A valid radiation input has be longer than 5 characters. Otherwise, no radiation.")
        radiation = input("Type ADDITIONAL radiation details: ")
        radiation = input2string(radiation, to_empty=True)
        if len(radiation) <= 5:
            icreate = 0
        else:
            icreate = 1
        if isinstance(previous_radiation,SNRadiation):
            radiation = merge_two_strings(previous_radiation.details, radiation)
        else:
            radiation = merge_two_strings(previous_radiation, radiation)
        thisobj = cls(radiation, icreate)
        return thisobj

    def __str__(self):
        return self.details

    def __repr__(self):
        return self.__str__()


class QRCode:
    def __init__(self, qrstring):
        qrstring = input2string(qrstring)
        self.qrstring = qrstring

    def generate_qrcode(self, foldname):
        filename = self.qrstring.split("_")
        filename = filename[-1]
        filename = filename + "_QR.png"
        img = qrcode.make(self.qrstring)
        img.save(filename)
        if not os.path.isdir(os.path.join(FILE_PATH, foldname)):
            os.makedirs(os.path.join(FILE_PATH, foldname))
        img.save(os.path.join(FILE_PATH, foldname, filename))

    def __str__(self):
        return self.qrstring

    def __repr__(self):
        return self.__str__()


class SNEntry:
    def __init__(self, comp, syns, char, integ, radiation, rgroup, yourname, paperlink, comments,
                 history, sdatetime, entryid, qrstring,
                 previous_nearestsample=None, upload_files=None):
        self.comp = comp
        self.syns = syns
        self.char = char
        self.integ = integ
        self.radiation = radiation
        self.rgroup = input2string(rgroup, to_empty=True)
        self.yourname = input2string(yourname, to_empty=True)
        self.paperlink = input2string(paperlink, to_empty=True)
        self.comments = input2string(comments, to_empty=True)
        if len(self.paperlink) < 10:
            self.paperlink = ""
        if len(history) == 0:
            history = str(entryid)
            firstsample = entryid
        else:
            hl = history.split(",")
            firstsample = int(hl[0])
            history += "," + str(entryid)
        self.firstsample = firstsample
        self.icreate = 0
        if self.integ.icreate == 1 or self.radiation.icreate == 1:
            self.icreate = 1
        if self.icreate == 0:
            if isinstance(previous_nearestsample, int):
                self.nearestsample = previous_nearestsample
            else:
                self.nearestsample = firstsample
        else:
            self.nearestsample = entryid
        self.history = history
        self.sdatetime = sdatetime
        self.entryid = entryid
        self.qrstring = qrstring

        self.foldname = comp.elementstr + "/" + syns.method
        if not os.path.isdir(os.path.join(FILE_PATH, self.foldname)):
            os.makedirs(os.path.join(FILE_PATH, self.foldname))

        self.fileheader = comp.commonname + "_" + syns.method + \
                          "_" + char.method + "_EID" + str(entryid)

        self.filelinks = "QRLink" + " "
        f = "EID" + str(self.entryid) + "_QR.png"
        thislink = os.path.join(FILE_PATH, self.foldname, f)
        self.nfiles = 0
        if isinstance(upload_files, list) and len(upload_files) > 0:
            self.uploading_files(upload_files)

    @classmethod
    def from_input(cls, upload_files=None):
        comp = SNComposition.from_input()
        syns = SNSynthesis.from_input()
        char = SNCharaterization.from_input()
        radiation = SNRadiation.from_input()
        integ = SampleIntegrity.from_input()
        paperlink = input("Type paper link (eg: https://doi.org/xx.xx.xx.xx): ")
        comments = input("Type your comments (eg: Section 2 from 1001): ")
        rgroup = input("Type PIs of research group (eg: first_lastname1, first_lastname2): ")
        yourname = input("Type your name (eg: Alice Smith): ")
        history = ""
        print("===========================================")
        confirm_input = input("Please confirm your input (Y for yes or N for No): ")
        confirm_input = input2string(confirm_input)
        while confirm_input[0].upper() != "Y":
            comp = SNComposition.from_input()
            syns = SNSynthesis.from_input()
            char = SNCharaterization.from_input()
            radiation = SNRadiation.from_input()
            paperlink = input("Type paper link (eg: https://doi.org/xx.xx.xx.xx): ")
            comments = input("Type your comments (eg: Section 2 from 1001): ")
            rgroup = input("Type PIs of research group (eg: first_lastname1, first_lastname2): ")
            yourname = input("Type your name (eg: Alice Smith): ")
            history = ""
            print("===========================================")
            confirm_input = input("Please confirm your input (Y for yes or N for No): ")
            confirm_input = input2string(confirm_input)
        sdatetime = str(datetime.datetime.now())
        entryid = get_nentries()
        entryid += 1
        write_nentries(entryid)
        print(f"=== Entry ID of this entry is {entryid} === .")
        foldname = comp.elementstr + "/" + syns.method
        qrstring = foldname + "_EID" + str(entryid)
        thisqr = QRCode(qrstring)
        thisqr.generate_qrcode(foldname)
        thisobj = cls(comp, syns, char, integ, radiation, rgroup, yourname, paperlink, comments,
                      history, sdatetime, entryid, qrstring,
                      previous_nearestsample=None, upload_files=upload_files)
        return thisobj

    @classmethod
    def from_history(cls, thisdict, upload_files=None):
        comp = SNComposition.from_history(thisdict["Composition"], str(thisdict["CommonName"]))
        syns = SNSynthesis.from_history(thisdict["Synthesis"], str(thisdict["SynDetails"]))
        char = SNCharaterization.from_history(thisdict["Characterization"], str(thisdict["CharDetails"]))
        radiation = SNRadiation.from_history(str(thisdict["RadiationDetails"]))
        integ = SampleIntegrity.from_history()
        paperlink = str(thisdict["PaperLink"])
        print("The existing paper link is " + paperlink + ".")
        newpaperlink = ""
        thisbool = get_bool_input()
        if thisbool:
            newpaperlink = input("Type paper link (eg: https://doi.org/xx.xx.xx.xx): ")
        paperlink = merge_two_strings(paperlink, newpaperlink, thres=10)
        comments = str(thisdict["Comments"])
        print("The existing comments are " + comments + ".")
        thisbool = get_bool_input()
        if thisbool:
            comments = input("Type your comments (eg: Section 2 from 1001): ")
        rgroup = input("Type PIs of research group (eg: first_lastname1, first_lastname2): ")
        yourname = input("Type your name (eg: Alice Smith): ")
        history = thisdict["History"]
        print("===========================================")
        confirm_input = input("Please confirm your input (Y for yes or N for No): ")
        confirm_input = input2string(confirm_input)
        while confirm_input[0].upper() != "Y":
            comp = SNComposition.from_history(thisdict["Composition"], str(thisdict["CommonName"]))
            syns = SNSynthesis.from_history(thisdict["Synthesis"], str(thisdict["SynDetails"]))
            char = SNCharaterization.from_history(thisdict["Characterization"], str(thisdict["CharDetails"]))
            radiation = SNRadiation.from_history(str(thisdict["RadiationDetails"]))
            integ = SampleIntegrity.from_history()
            paperlink = str(thisdict["PaperLink"])
            print("The existing paper link is " + paperlink + ".")
            newpaperlink = ""
            thisbool = get_bool_input()
            if thisbool:
                newpaperlink = input("Type paper link (eg: https://doi.org/xx.xx.xx.xx): ")
            paperlink = merge_two_strings(paperlink, newpaperlink, thres=10)
            comments = str(thisdict["Comments"])
            print("The existing comments are " + comments + ".")
            thisbool = get_bool_input()
            if thisbool:
                comments = input("Type your comments (eg: Section 2 from 1001): ")
            rgroup = input("Type PIs of research group (eg: first_lastname1, first_lastname2): ")
            yourname = input("Type your name (eg: Alice Smith): ")
            history = thisdict["History"]
            print("===========================================")
            confirm_input = input("Please confirm your input (Y for yes or N for No): ")
            confirm_input = input2string(confirm_input)
        sdatetime = str(datetime.datetime.now())
        entryid = get_nentries()
        entryid += 1
        write_nentries(entryid)
        print(f"=== Entry ID of this entry is {entryid} === .")
        foldname = thisdict["FileFolder"]
        qrstring = foldname + "_EID" + str(entryid)
        thisqr = QRCode(qrstring)
        thisqr.generate_qrcode(foldname)
        thisobj = cls(comp, syns, char, integ, radiation, rgroup, yourname, paperlink, comments,
                      history, sdatetime, entryid, qrstring,
                      previous_nearestsample=thisdict["NearestSampleID"], upload_files=upload_files)
        return thisobj

    def uploading_files(self, upload_files):
        if isinstance(upload_files, list) and len(upload_files) > 0:
            for i in range(len(upload_files)):
                sf = upload_files[i]
                if "." in sf:
                    app = sf.split(".")
                    app = app[-1]
                else:
                    app = "none"
                tf = self.fileheader + "_F" + str(self.nfiles + 1)
                tf = tf + "." + app
                self.filelinks += "FileLink" + str(self.nfiles + 1) + " "
                thislink = os.path.join(FILE_PATH, self.foldname, tf)
                shutil.copy(sf, os.path.join(FILE_PATH, self.foldname, tf))
                self.nfiles += 1

    def to_dict(self):
        thisdict = {}
        for i in range(len(CSV_HEADERS)):
            key = CSV_HEADERS[i]
            if key == "Elements":
                thisdict[key] = self.comp.elementstr
            elif key == "Composition":
                thisdict[key] = self.comp.compstr
            elif key == "CommonName":
                thisdict[key] = self.comp.commonname
            elif key == "Synthesis":
                thisdict[key] = self.syns.method
            elif key == "SynDetails":
                thisdict[key] = self.syns.details
            elif key == "Characterization":
                thisdict[key] = self.char.method
            elif key == "CharDetails":
                thisdict[key] = self.char.details
            elif key == "iUsage":
                thisdict[key] = self.integ.iusage
            elif key == "iCreate":
                thisdict[key] = self.icreate
            elif key == "RadiationDetails":
                thisdict[key] = self.radiation.details
            elif key == "ResearchGroup":
                thisdict[key] = self.rgroup
            elif key == "YourName":
                thisdict[key] = self.yourname
            elif key == "PaperLink":
                thisdict[key] = self.paperlink
            elif key == "Comments":
                thisdict[key] = self.comments
            elif key == "QRString":
                thisdict[key] = self.qrstring
            elif key == "DateTime":
                thisdict[key] = self.sdatetime
            elif key == "nFiles":
                thisdict[key] = self.nfiles
            elif key == "FileFolder":
                thisdict[key] = self.foldname
            elif key == "FileHeader":
                thisdict[key] = self.fileheader
            elif key == "FileLinks":
                thisdict[key] = self.filelinks
            elif key == "EntryID":
                thisdict[key] = self.entryid
            elif key == "FirstSampleID":
                thisdict[key] = self.firstsample
            elif key == "NearestSampleID":
                thisdict[key] = self.nearestsample
            elif key == "History":
                thisdict[key] = self.history
        return thisdict

    def __str__(self):
        return f"entryid: {self.entryid}  history: {self.history}  nearestsampleid: {self.nearestsample}."

    def __repr__(self):
        return self.__str__()
