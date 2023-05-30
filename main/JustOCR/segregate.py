import cv2
import numpy as np
import ftfy
import pytesseract
from PIL import Image
import regex
from fuzzywuzzy import fuzz


def OCR(imgpath):
    """returns OCR text in a string"""
    img = cv2.imread(imgpath)
    # img = cv2.resize(img, None, fx=2, fy=2,interpolation=cv2.INTER_CUBIC)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    pytesseract.pytesseract.tesseract_cmd = 'C:/Program Files/Tesseract-OCR/tesseract.exe'
    text = pytesseract.image_to_string(img, lang = 'eng+hin')
    text = ftfy.fix_text(text)
    text = ftfy.fix_encoding(text)
    return text

def fuzzMatch( major, minor, errs = 4, threshold = 65 ):
    """Checks if arg2 string is in arg1 string"""
    if(len(major)<1):
        return 0 
    errs_ = 0
    major = major.lower()
    minor = minor.lower()
    s = regex.search(f"({minor}){{e<={errs_}}}", major)
    while s is None and errs_ <= errs:
        errs_ += 1
        s = regex.search(f"({minor}){{e<={errs_}}}", major)
    if(fuzz.token_set_ratio(minor,s.group())>threshold):
        return 1
    else:
        return 0
    

idKeyWords = {"PAN":["income","permanent","account"],"DL":["driving","drive","dl no","transport"], "Passport": ["republic","passport"],"Aadhaar":["aadhaar","आधार","uidai"]}


def classify(text):
    """classifies the images based on input OCR text
    - Input: OCR text in image {extracted using OCR function}
    - Returns: string of document names
    """
    for key in idKeyWords:
        for word in idKeyWords[key]:
            if(fuzzMatch(text,word)):
                return key
    return "other"    
    

def segregate(filepaths):
    """
    uses OCR pytesseract to classify the image
    
    eg:
    - Input:
        - filepaths = ["aadhar.png","aadharlk.png","aadharlkb.png","pan.jpg"]
    - Returns:
        - {'PAN': ['pan.jpg'],
        'DL': [ ],
        'Passport': [ ],
        'Aadhaar': ['aadhar.png', 'aadharlk.png', 'aadharlkb.png'],
        'other': [ ]}
    ----------
    Takes an list of imagePaths as Input \\
    and Outputs a dictionary having 5 keys:
    - PAN
    - DL
    - Passport
    - Aadhaar
    - other
    
    with an list of filepaths as values
    
    """
    classifiedDict = {"PAN":[],"DL":[],"Passport":[],"Aadhaar":[],"other":[]}
    for path in filepaths:
        ocrTxt = OCR(path).lower()
        doctype = classify(ocrTxt)
        if(doctype=="other"):
            res = ocrTxt.split()
            for i in range(len(res) - 1):
                check = 1
                for j in range(3):
                    check = check and len(res[i+j]) == 4 and res[i+j].isdigit()
                # check = check and ("male" in res or "female" in res)
                if(check):
                    doctype = "Aadhaar"
        classifiedDict[doctype].append(path)
    return classifiedDict