import os
import qrcode
import shutil
#import time
import datetime
from samplenaming.core.snglobal import Synthesis, Characterization
from samplenaming.core.snglobal import FILE_PATH, CSV_HEADERS
from samplenaming.core.config import get_nentries, write_nentries
from samplenaming.periodictable.composition import Composition


def input2string(instring):
    instring = str(instring)
    if instring is None:
        instring = "nan"
    elif len(instring) == 0:
        instring = "nan"
    elif str(instring).upper() == "NAN":
        instring = "nan"
    instring = instring.strip()
    instring = instring.replace("|", ",")
    return instring


def get_bool_input():
    thisbool = input("Want to modify (Y for yes and N for no)?")
    thisbool = input2string(thisbool)
    if thisbool[0].upper() == "Y":
        thisbool = True
    else:
        thisbool = False
    return thisbool

def get_comfirm_bool():
    thisbool = input("Please confirm your input (Y for yes and N for no)?")
    thisbool = input2string(thisbool)
    if thisbool[0].upper() == "Y":
        thisbool = True
    else:
        thisbool = False
    return thisbool


class SNComposition:
    def __init__(self, compstr, commonname=None):
        compstr = input2string(compstr)
        comp = Composition(compstr)
        comp = Composition(comp.reduced_formula)
        self.compstr = comp.reduced_formula
        self.elementstr = ""
        for el in comp.elements:
            self.elementstr += el.symbol
        commonname = input2string(commonname)
        #commonname = commonname.replace(" ", "")
        #commonname = commonname.replace("/", "_")
        #commonname = commonname.replace("\\", "_")
        if str(commonname).upper() == "NAN":
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
        thisobj = cls(compstr, commonname)
        return thisobj

    @classmethod
    def from_history(cls, compstr, commonname):
        print(f"The existing composition is {compstr}.")
        print("WARNING: Modification of composition is NOT recommended.")
        thisbool = get_bool_input()
        if thisbool:
            compstr = input("Type composition (eg: H2O): ")
            compstr = input2string(compstr)
            print(f"Your composition is {compstr}.")
            thisbool = get_comfirm_bool()
            while not thisbool:
                compstr = input("Type composition (eg: H2O): ")
                compstr = input2string(compstr)
                print(f"Your composition is {compstr}.")
                thisbool = get_comfirm_bool()
        print(f"The existing common name is {commonname}.")
        thisbool = get_bool_input()
        if thisbool:
            commonname = input("Type common name (eg: TTHZ): ")
        thisobj = cls(input2string(compstr), input2string(commonname))
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
        self.details = input2string(details)

    @classmethod
    def from_input(cls):
        print("List of synthesis methods: ")
        for i in range(len(Synthesis)):
            print(f"{i+1} -- {Synthesis[i]}")

        instr = input("Select method (eg: 1): ")
        instr = input2string(instr)
        while not instr[0].isdigit():
            instr = input("Select method (eg: 1): ")
            instr = input2string(instr)
        try:
            method = Synthesis[int(instr[0])-1]
        except:
            method = "Unknown"
        if method == "Unknown":
            details = "nan"
        else:
            details = input(f"Type details of {method}: ")
        thisobj = cls(method, details)
        return thisobj

    @classmethod
    def from_history(cls, method, details):
        print(f"The existing synthesis method is {method}.")
        print("WARNING: Modification of synthesis method is NOT recommended.")
        thisbool = get_bool_input()
        if thisbool:
            print("List of synthesis methods: ")
            for i in range(len(Synthesis)):
                print(f"{i + 1} -- {Synthesis[i]}")
            instr = input("Select method (eg: 1): ")
            instr = input2string(instr)
            while not instr[0].isdigit():
                instr = input("Select method (eg: 1): ")
                instr = input2string(instr)
            try:
                method = Synthesis[int(instr[0]) - 1]
            except:
                method = "Unknown"
        if method == "Unknown":
            details = "nan"
        else:
            print(f"The existing details for {method} is {details}.")
            print("WARNING: Modification of synthesis details is NOT recommended.")
            thisbool = get_bool_input()
            if thisbool:
                details = input(f"Type details of {method}: ")
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
            print(f"{i+1} -- {Characterization[i]}")

        instr = input("Select method (eg: 1): ")
        instr = input2string(instr)
        while not instr[0].isdigit():
            instr = input("Select method (eg: 1): ")
            instr = input2string(instr)
        try:
            method = Characterization[int(instr[0])-1]
        except:
            method = "Unknown"

        if method == "Unknown":
            details = "nan"
        else:
            details = input(f"Type details of {method}: ")
        thisobj = cls(method, details)
        return thisobj

    @classmethod
    def from_history(cls, method, details):
        print(f"The existing characterization method is {method}.")
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
            print(f"The existing details for {method} is {details}.")
            thisbool = get_bool_input()
            if thisbool:
                details = input(f"Type details of {method}: ")
        thisobj = cls(method, details)
        return thisobj

    def __str__(self):
        return f"Charact. method: {self.method} details: {self.details}."

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
        return f"QR string: {self.qrstring}."

    def __repr__(self):
        return self.__str__()


class SNEntry:
    def __init__(self, comp, syns, char, radiation, rgroup, yourname, paperlink, comments,
                 history, sdatetime, entryid, qrstring,
                 foldname=None, upload_files=None):
        self.comp = comp
        self.syns = syns
        self.char = char
        self.radiation = input2string(radiation)
        self.rgroup = input2string(rgroup)
        self.yourname = input2string(yourname)
        self.paperlink = input2string(paperlink)
        self.comments = input2string(comments)
        if len(self.paperlink) < 10:
            self.paperlink = ""
        if len(history) == 0:
            history = str(entryid)
            firstentry = entryid
        else:
            hl = history.split(",")
            firstentry = int(hl[0])
            history += "," + str(entryid)
        self.firstentry = firstentry
        self.history = history
        self.sdatetime = sdatetime
        self.entryid = entryid
        self.qrstring = qrstring
        if foldname is None:
            self.foldname = comp.elementstr + "/" + syns.method
            if not os.path.isdir(os.path.join(FILE_PATH, self.foldname)):
                os.makedirs(os.path.join(FILE_PATH, self.foldname))
        else:
            self.foldname = foldname
        self.fileheader = comp.compstr + "_" + syns.method + \
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
        radiation = input("Type radiation details: ")
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
            radiation = input("Type radiation details: ")
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
        thisobj = cls(comp, syns, char, radiation, rgroup, yourname, paperlink, comments,
                      history, sdatetime, entryid, qrstring,
                      foldname=None, upload_files=upload_files)
        return thisobj

    @classmethod
    def from_history(cls, thisdict, upload_files=None):
        comp = SNComposition.from_history(thisdict["Composition"], thisdict["CommonName"])
        syns = SNSynthesis.from_history(thisdict["Synthesis"], thisdict["SynDetails"])
        char = SNCharaterization.from_history(thisdict["Characterization"], thisdict["CharDetails"])
        radiation = thisdict["RadiationDetails"]
        print(f"The existing radiation details are {radiation}.")
        thisbool = get_bool_input()
        if thisbool:
            radiation = input("Type radiation details: ")
        paperlink = thisdict["PaperLink"]
        print(f"The existing paper link is {paperlink}.")
        thisbool = get_bool_input()
        if thisbool:
            paperlink = input("Type paper link (eg: https://doi.org/xx.xx.xx.xx): ")
        comments = thisdict["Comments"]
        print(f"The existing comments are {comments}.")
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
            comp = SNComposition.from_history(thisdict["Composition"], thisdict["CommonName"])
            syns = SNSynthesis.from_history(thisdict["Synthesis"], thisdict["SynDetails"])
            char = SNCharaterization.from_history(thisdict["Characterization"], thisdict["CharDetails"])
            radiation = thisdict["RadiationDetails"]
            print(f"The existing radiation details are {radiation}.")
            thisbool = get_bool_input()
            if thisbool:
                radiation = input("Type radiation details: ")
            paperlink = thisdict["PaperLink"]
            print(f"The existing paper link is {paperlink}.")
            thisbool = get_bool_input()
            if thisbool:
                paperlink = input("Type paper link (eg: https://doi.org/xx.xx.xx.xx): ")
            comments = thisdict["Comments"]
            print(f"The existing comments are {comments}.")
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
        thisobj = cls(comp, syns, char, radiation, rgroup, yourname, paperlink, comments,
                      history, sdatetime, entryid, qrstring,
                      foldname=foldname, upload_files=upload_files)
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
            elif key == "RadiationDetails":
                thisdict[key] = self.radiation
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
            elif key == "FirstEntryID":
                thisdict[key] = self.firstentry
            elif key == "FileLinks":
                thisdict[key] = self.filelinks
            elif key == "EntryID":
                thisdict[key] = self.entryid
            elif key == "History":
                thisdict[key] = self.history
        return thisdict

    def __str__(self):
        return f"entryid: {self.entryid} fileheader: {self.fileheader} history: {self.history}."

    def __repr__(self):
        return self.__str__()
