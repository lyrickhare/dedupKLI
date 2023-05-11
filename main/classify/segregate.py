import cv2
import numpy as np
import ftfy
import pytesseract
from PIL import Image
import regex
from fuzzywuzzy import fuzz


def OCR(imgpath):
    img = cv2.imread(imgpath)
    img = cv2.resize(img, None, fx=2, fy=2,interpolation=cv2.INTER_CUBIC)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    pytesseract.pytesseract.tesseract_cmd = 'C:/Program Files/Tesseract-OCR/tesseract.exe'
    text = pytesseract.image_to_string(img, lang = 'eng+hin')
    text = ftfy.fix_text(text)
    text = ftfy.fix_encoding(text)
    return text

def fuzzMatch( major, minor, errs = 4, threshold = 65 ):
    errs_ = 0
    major = major.lower()
    minor = minor.lower()
    s = regex.search(f"({minor}){{e<={errs_}}}", major)
    while s is None and errs_ <= errs:
        errs_ += 1
        s = regex.search(f"({minor}){{e<={errs_}}}", major)
    if(fuzz.token_set_ratio(minor,s)>threshold):
        return 1
    else:
        return 0
    

idKeyWords = {"PAN":["income","permanent","account"],"DL":["driving","drive","dl no","transport"], "Passport": ["republic","passport"],"Aadhaar":["aadhaar"]}


def classify(text):
    for key in idKeyWords:
        for word in idKeyWords[key]:
            if(fuzzMatch(text,word)):
                return key
    return "other"    
    

def segregate(filepaths):
    classifiedDict = {"PAN":[],"DL":[],"Passport":[],"Aadhaar":[],"other":[]}
    for path in filepaths:
        ocrTxt = OCR(path)
        doctype = classify(ocrTxt)
        if(doctype=="other"):
            res = ocrTxt.split()
            for i in range(len(res) - 1):
                check = 1
                for j in range(3):
                    check = check and len(res[i+j]) == 4 and res[i+j].isdigit()
                check = check and ("male" in res or "MALE" in res)
                if(check):
                    doctype = "Aadhaar"
        classifiedDict[doctype].append(path)
    return classifiedDict