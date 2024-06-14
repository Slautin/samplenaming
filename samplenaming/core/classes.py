import os
import qrcode
import shutil
import json
import time
import datetime
from samplenaming.core.snglobal import Synthesis, Characterization, ResearchGroup
from samplenaming.core.snglobal import FILE_PATH, CSV_HEADERS
from samplenaming.core.config import get_nentries, write_nentries
from samplenaming.periodictable.composition import Composition


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
    def __init__(self, comp, syns, char, rgroup, qrstring, sampleid, sdatetime, initials="NA", comments="NA"):
        self.comp = comp
        self.syns = syns
        self.char = char
        self.rgroup = rgroup
        self.qrstring = qrstring
        self.sampleid = sampleid
        self.sdatetime = sdatetime
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
        nanosec = time.time_ns()
        comp = SNComposition.from_input()
        syns = SNSynthesis.from_input()
        char = SNCharaterization.from_input()
        rgroup = SNResearchgroup.from_input()
        foldname = comp.elementstr + "/" + "S" + syns.ID
        qrstring = foldname + "_T" + str(nanosec)
        thisqr = QRCode(qrstring)
        thisqr.generate_qrcode(foldname)
        initials = input("Type your name initial: ")
        initials = initials.strip()
        initials = initials.replace("|", ",")
        comments = input("Type comments: ")
        comments = comments.strip()
        comments = comments.replace("|", ",")
        sampleid = get_nentries()
        sampleid += 1
        write_nentries(sampleid)
        sdatetime = str(datetime.datetime.now())
        thisobj = cls(comp, syns, char, rgroup, qrstring, sampleid, sdatetime, initials=initials, comments=comments)

        if isinstance(upload_files, list) and len(upload_files) > 0:
            for i in range(len(upload_files)):
                sf = upload_files[i]
                if "." in sf:
                    app = sf.split(".")
                    app = app[-1]
                else:
                    app = "none"
                tf = thisobj.filename + "_T" + str(nanosec) + "_F" + str(thisobj.nfiles + 1)
                tf = tf + "." + app
                shutil.copy(sf, os.path.join(FILE_PATH, thisobj.foldname, tf))
                thisobj.nfiles += 1

        return thisobj

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
            elif key == "SynParams":
                tmpstr = json.dumps(self.syns.params)
                tmpstr = tmpstr.strip()
                tmpstr = tmpstr.replace("|", ",")
                thisdict[key] = tmpstr
            elif key == "Characterization":
                thisdict[key] = self.char.method
            elif key == "CharParams":
                tmpstr = json.dumps(self.char.params)
                tmpstr = tmpstr.strip()
                tmpstr = tmpstr.replace("|", ",")
                thisdict[key] = tmpstr
            elif key == "ResearchGroup":
                thisdict[key] = self.rgroup.PIs
            elif key == "QRcode":
                thisdict[key] = self.qrstring
            elif key == "Initials":
                thisdict[key] = self.initials
            elif key == "Comments":
                thisdict[key] = self.comments
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
