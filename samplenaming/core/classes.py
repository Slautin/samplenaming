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
    instring = instring.strip()
    instring = instring.replace("|", ",")
    return instring


class SNComposition:
    def __init__(self, compstr):
        comp = Composition(compstr)
        comp = Composition(comp.reduced_formula)
        self.compstr = comp.reduced_formula
        self.elementstr = ""
        for el in comp.elements:
            self.elementstr += el.symbol

    @classmethod
    def from_input(cls):
        compstr = input("Type composition (eg: H2O): ")
        thisobj = cls(compstr)
        return thisobj

    @classmethod
    def from_history(cls, compstr):
        print(f"The existing composition is {compstr}.")
        thisbool = input("Want to modify (Y for yes and N for no)?")
        if thisbool[0].upper() == "Y":
            thisbool = True
        else:
            thisbool = False
        if thisbool:
            compstr = input("Type composition (eg: H2O): ")
        thisobj = cls(compstr)
        return thisobj

    def __str__(self):
        return f"The elementstr: {self.elementstr} compstr: {self.compstr}."

    def __repr__(self):
        return self.__str__()


class SNSynthesis:
    def __init__(self, method, details):
        self.method = method
        if self.method == "Unknown":
            details = "NA"
        self.details = input2string(details)

    @classmethod
    def from_input(cls):
        print("List of synthesis methods: ")
        for i in range(len(Synthesis)):
            print(f"{i+1} -- {Synthesis[i]}")

        instr = input("Select method (eg: 1): ")
        instr = instr.strip()
        try:
            method = Synthesis[int(instr)-1]
        except:
            method = "Unknown"
        if method == "Unknown":
            details = "NA"
        else:
            details = input(f"Type details of {method}: ")
        thisobj = cls(method, details)
        return thisobj

    @classmethod
    def from_history(cls, method, details):
        print(f"The existing method is {method}.")
        thisbool = input("Want to modify (Y for yes and N for no)?")
        if thisbool[0].upper() == "Y":
            thisbool = True
        else:
            thisbool = False
        if thisbool:
            print("List of synthesis methods: ")
            for i in range(len(Synthesis)):
                print(f"{i + 1} -- {Synthesis[i]}")

            instr = input("Select method (eg: 1): ")
            instr = instr.strip()
            try:
                method = Synthesis[int(instr) - 1]
            except:
                method = "Unknown"
        if method == "Unknown":
            details = "NA"
        else:
            print(f"The existing details for {method} is {details}.")
            thisbool = input("Want to modify (Y for yes and N for no)?")
            if thisbool[0].upper() == "Y":
                thisbool = True
            else:
                thisbool = False
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
            details = "NA"
        self.details = input2string(details)

    @classmethod
    def from_input(cls):
        print("List of synthesis methods: ")
        for i in range(len(Characterization)):
            print(f"{i+1} -- {Characterization[i]}")

        instr = input("Select method (eg: 1): ")
        instr = instr.strip()
        try:
            method = Characterization[int(instr)-1]
        except:
            method = "Unknown"

        if method == "Unknown":
            details = "NA"
        else:
            details = input(f"Type details of {method}: ")
        thisobj = cls(method, details)
        return thisobj

    @classmethod
    def from_history(cls, method, details):
        print(f"The existing method is {method}.")
        thisbool = input("Want to modify (Y for yes and N for no)?")
        if thisbool[0].upper() == "Y":
            thisbool = True
        else:
            thisbool = False
        if thisbool:
            print("List of synthesis methods: ")
            for i in range(len(Characterization)):
                print(f"{i + 1} -- {Characterization[i]}")

            instr = input("Select method (eg: 1): ")
            instr = instr.strip()
            try:
                method = Characterization[int(instr) - 1]
            except:
                method = "Unknown"

        if method == "Unknown":
            details = "NA"
        else:
            print(f"The existing details for {method} is {details}.")
            thisbool = input("Want to modify (Y for yes and N for no)?")
            if thisbool[0].upper() == "Y":
                thisbool = True
            else:
                thisbool = False
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
    def __init__(self, comp, syns, char, qrstring, sampleid, sdatetime, rgroup, initials="NA", history=None):
        self.comp = comp
        self.syns = syns
        self.char = char
        self.qrstring = qrstring
        self.sampleid = sampleid
        self.sdatetime = sdatetime
        self.rgroup = input2string(rgroup)
        self.initials = input2string(initials)
        self.history = input2string(history)
        self.history = self.history.replace("/", "->")
        self.history = self.history.replace("\\", "->")
        self.history = self.history.replace("_", "->")

        self.foldname = comp.elementstr + "/" + syns.method
        if not os.path.isdir(os.path.join(FILE_PATH, self.foldname)):
            os.makedirs(os.path.join(FILE_PATH, self.foldname))
        files = os.listdir(os.path.join(FILE_PATH, self.foldname))
        self.nfiles = len(files)
        self.filename = comp.compstr + "_" + syns.method + "_" + char.method + "_H" + str(self.history)

    @classmethod
    def from_input(cls, upload_files=None):
        sampleid = get_nentries()
        sampleid += 1
        write_nentries(sampleid)
        print(f"=== Sample ID of this entry is {sampleid} === .")
        sdatetime = str(datetime.datetime.now())

        comp = SNComposition.from_input()
        syns = SNSynthesis.from_input()
        char = SNCharaterization.from_input()
        foldname = comp.elementstr + "/" + syns.method
        qrstring = foldname + "_SID" + str(sampleid)
        thisqr = QRCode(qrstring)
        thisqr.generate_qrcode(foldname)
        rgroup = input("Type PIs of research group (eg: firstname1_lastname1 + firstname2_lastname2): ")
        initials = input("Type your name initial (eg: ZW): ")
        history = input("Type sample history (eg: SID1003, SID1010): ")

        thisobj = cls(comp, syns, char, qrstring, sampleid, sdatetime, rgroup, initials=initials, history=history)
        if isinstance(upload_files, list) and len(upload_files) > 0:
            thisobj.uploading_files(upload_files)
        return thisobj

    @classmethod
    def from_history(cls, thisdict, upload_files=None):
        sampleid = get_nentries()
        sampleid += 1
        write_nentries(sampleid)
        print(f"=== Sample ID of this entry is {sampleid} === .")
        sdatetime = str(datetime.datetime.now())

        comp = SNComposition.from_history(thisdict["Composition"])
        syns = SNSynthesis.from_history(thisdict["Synthesis"], thisdict["SynDetails"])
        char = SNCharaterization.from_history(thisdict["Characterization"], thisdict["CharDetails"])
        foldname = comp.elementstr + "/" + syns.method
        qrstring = foldname + "_SID" + str(sampleid)
        thisqr = QRCode(qrstring)
        thisqr.generate_qrcode(foldname)

        history = thisdict["History"]
        print(f"The existing sample history is {history}.")
        thisbool = input("Want to modify (Y for yes and N for no)?")
        if thisbool[0].upper() == "Y":
            thisbool = True
        else:
            thisbool = False
        if thisbool:
            history = input("Type sample history (eg: SID1003, SID1010): ")
        rgroup = input("Type PIs of research group (eg: firstname1_lastname1 + firstname2_lastname2): ")
        initials = input("Type your name initial (eg: ZW): ")
        thisobj = cls(comp, syns, char, qrstring, sampleid, sdatetime, rgroup, initials=initials, history=history)
        if isinstance(upload_files, list) and len(upload_files) > 0:
            thisobj.uploading_files(upload_files)
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
                tf = self.filename + "_SID" + str(self.sampleid) + "_F" + str(self.nfiles + 1)
                tf = tf + "." + app
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
            elif key == "Synthesis":
                thisdict[key] = self.syns.method
            elif key == "SynDetails":
                thisdict[key] = self.syns.details
            elif key == "Characterization":
                thisdict[key] = self.char.method
            elif key == "CharDetails":
                thisdict[key] = self.char.details
            elif key == "ResearchGroup":
                thisdict[key] = self.rgroup
            elif key == "QRcode":
                thisdict[key] = self.qrstring
            elif key == "Initials":
                thisdict[key] = self.initials
            elif key == "History":
                thisdict[key] = self.history
            elif key == "DateTime":
                thisdict[key] = self.sdatetime
            elif key == "nFiles":
                thisdict[key] = self.nfiles
            elif key == "SampleFolder":
                thisdict[key] = self.foldname
            elif key == "SampleName":
                thisdict[key] = self.filename
            elif key == "SampleID":
                thisdict[key] = self.sampleid
        return thisdict

    def __str__(self):
        return f"sampleid: {self.sampleid} foldname:{self.foldname} filename: {self.filename}."

    def __repr__(self):
        return self.__str__()
