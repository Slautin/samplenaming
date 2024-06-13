import os
import qrcode
import shutil
import json
from samplenaming.periodictable.composition import Composition
from samplenaming.core.snglobal import FILE_PATH, NANOTIME
from samplenaming.core.snglobal import CSV_HEADERS
from samplenaming.core.snglobal import Synthesis, Characterization, ResearchGroup


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

    def __str__(self):
        return f"The elementstr: {self.elementstr} compstr: {self.compstr}."

    def __repr__(self):
        return self.__str__()


class SNSynthesis:
    def __init__(self, thisdict):
        for key, value in thisdict.items():
            self.method = key
            self.params = value
        self.ID = self.params["ID"]

    @classmethod
    def from_input(cls):
        thisdict = {}
        print("List of synthesis methods: ")
        indict = {}
        i = 1
        for key in Synthesis:
            print(f"{i} -- {key}")
            indict[str(i)] = key
            i += 1
        instr = input("Select method (eg: 1): ")
        instr = instr.strip()
        method = indict[instr]
        indict = {}
        for key in Synthesis[method]:
            if key == "ID":
                indict[key] = Synthesis[method][key]
            else:
                instr = input(f"Type {key} setting: ")
                instr = instr.strip()
                instr = instr.replace("|", ",")
                indict[key] = instr
        thisdict[method] = indict
        thisobj = cls(thisdict)
        return thisobj

    def __str__(self):
        return f"Synthesis method: {self.method} params: {self.params}."

    def __repr__(self):
        return self.__str__()


class SNCharaterization:
    def __init__(self, thisdict):
        for key, value in thisdict.items():
            self.method = key
            self.params = value
        self.ID = self.params["ID"]

    @classmethod
    def from_input(cls):
        thisdict = {}
        print("List of characterization methods: ")
        indict = {}
        i = 1
        for key in Characterization:
            print(f"{i} -- {key}")
            indict[str(i)] = key
            i += 1
        instr = input("Select method (eg: 1): ")
        instr = instr.strip()
        method = indict[instr]
        indict = {}
        for key in Characterization[method]:
            if key == "ID":
                indict[key] = Characterization[method][key]
            else:
                instr = input(f"Type {key} setting: ")
                instr = instr.strip()
                instr = instr.replace("|", ",")
                indict[key] = instr
        thisdict[method] = indict
        thisobj = cls(thisdict)
        return thisobj

    def __str__(self):
        return f"Charact. method: {self.method} params: {self.params}."

    def __repr__(self):
        return self.__str__()


class SNResearchgroup:
    def __init__(self, thisdict):
        for key, value in thisdict.items():
            self.PIs = key
            self.params = value
        self.ID = self.params["ID"]

    @classmethod
    def from_input(cls):
        thisdict = {}
        print("List of research groups: ")
        indict = {}
        i = 1
        for key in ResearchGroup:
            print(f"{i} -- {key}")
            indict[str(i)] = key
            i += 1
        instr = input("Select research group (eg: 1): ")
        instr = instr.strip()
        pis = indict[instr]
        indict = {}
        for key in ResearchGroup[pis]:
            if key == "ID":
                indict[key] = ResearchGroup[pis][key]
            else:
                instr = input(f"Type {key} setting: ")
                instr = instr.strip()
                instr = instr.replace("|", ",")
                indict[key] = instr
        thisdict[pis] = indict
        thisobj = cls(thisdict)
        return thisobj

    def __str__(self):
        return f"Research PIs: {self.PIs} params: {self.params}."

    def __repr__(self):
        return self.__str__()


class QRCode:
    def __init__(self, qrstring):
        self.qrstring = qrstring
        instrs = qrstring.split("_")
        self.foldname = instrs[0]
        self.filename = instrs[-1] + "_QR.png"

    def generate_qrcode(self):
        img = qrcode.make(self.qrstring)
        img.save(self.filename)
        if not os.path.isdir(os.path.join(FILE_PATH, self.foldname)):
            os.makedirs(os.path.join(FILE_PATH, self.foldname))
        img.save(os.path.join(FILE_PATH, self.foldname, self.filename))

    def __str__(self):
        return f"QR string: {self.qrstring} foldname: {self.foldname} filename: {self.filename}."

    def __repr__(self):
        return self.__str__()


class SNEntry:
    def __init__(self, comp, syns, char, rgroup, qrstring, initials="NA", comments="NA"):
        self.comp = comp
        self.syns = syns
        self.char = char
        self.rgroup = rgroup
        self.qrstring = qrstring
        self.initials = initials
        self.comments = comments
        self.foldname = comp.elementstr + "/" + "S" + syns.ID
        if not os.path.isdir(os.path.join(FILE_PATH, self.foldname)):
            os.makedirs(os.path.join(FILE_PATH, self.foldname))
        files = os.listdir(os.path.join(FILE_PATH, self.foldname))
        self.nfiles = len(files)
        self.filename = comp.compstr + "_S" + syns.ID + "_C" + char.ID

    @classmethod
    def from_input(cls, upload_files=None):
        comp = SNComposition.from_input()
        syns = SNSynthesis.from_input()
        char = SNCharaterization.from_input()
        rgroup = SNResearchgroup.from_input()
        qrstring = comp.elementstr + "/" + "S" + syns.ID
        qrstring += "_T" + str(NANOTIME)
        thisqr = QRCode(qrstring)
        thisqr.generate_qrcode()
        initials = input("Type your name initial: ")
        initials = initials.strip()
        initials = initials.replace("|", ",")
        comments = input("Type comments: ")
        comments = comments.strip()
        comments = comments.replace("|", ",")
        thisobj = cls(comp, syns, char, rgroup, qrstring, initials=initials, comments=comments)
        if isinstance(upload_files, list) and len(upload_files) > 0:
            thisobj.uploading_files(upload_files)
        return thisobj

    def uploading_files(self, upload_files):
        for i in range(len(upload_files)):
            sf = upload_files[i]
            app = sf.split(".")
            app = app[-1]
            tf = self.filename + "_F" + str(self.nfiles+1) + "_T" + str(NANOTIME)
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
            elif key == "SynID":
                thisdict[key] = self.syns.ID
            elif key == "SynParams":
                tmpstr = json.dumps(self.syns.params)
                tmpstr = tmpstr.strip()
                tmpstr = tmpstr.replace("|", ",")
                thisdict[key] = tmpstr
            elif key == "Characterization":
                thisdict[key] = self.char.method
            elif key == "CharID":
                thisdict[key] = self.char.ID
            elif key == "CharParams":
                tmpstr = json.dumps(self.char.params)
                tmpstr = tmpstr.strip()
                tmpstr = tmpstr.replace("|", ",")
                thisdict[key] = tmpstr
            elif key == "ResearchGroup":
                thisdict[key] = self.rgroup.PIs
            elif key == "GroupID":
                thisdict[key] = self.rgroup.ID
            elif key == "QRcode":
                thisdict[key] = self.qrstring
            elif key == "Initials":
                thisdict[key] = self.initials
            elif key == "Comments":
                thisdict[key] = self.comments
            elif key == "SampleFolder":
                thisdict[key] = self.foldname
            elif key == "SampleName":
                thisdict[key] = self.filename
            elif key == "nFiles":
                thisdict[key] = self.nfiles
        return thisdict

    def __str__(self):
        return f"filename: {self.filename} QRstring: {self.qrstring} foldname: {self.foldname} nfiles: {self.nfiles}."

    def __repr__(self):
        return self.__str__()
