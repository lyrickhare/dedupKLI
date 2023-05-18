import cv2
import numpy as np
import ftfy
import pytesseract
from PIL import Image
import regex
from fuzzywuzzy import fuzz
import clean


def OCR(imgpath):
    """returns OCR text in a string"""

    img = cv2.imread(imgpath, cv2.IMREAD_COLOR)
    
    obj = clean.doc()
    img = obj.rotate(img)
    img = obj.contrast_image(img)
    # txt = []
    txt0 = pytesseract.image_to_string(img, lang = 'eng+hin',config="--psm 6")
    txt1 = pytesseract.image_to_string(img, lang = 'eng+hin',config="--psm 4")
    txt2 = pytesseract.image_to_string(img, lang = 'eng+hin',config="--psm 3")
    txt3 = pytesseract.image_to_string(img, lang = 'eng+hin',config="--psm 12")
    # text = txt[0]+txt[1]+txt[2]
    text = txt0 + txt1 + txt2 + txt3

    text = ftfy.fix_text(text)
    text = ftfy.fix_encoding(text)
    print("ocrdone "+imgpath)
    return text

    # img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    # a = [3,4,6]
    # txt=[]
    # for i in range(len(a)):
    # txt[i]=obj.text_extractor(img,i)
    # img = cv2.resize(img, None, fx=2, fy=2,interpolation=cv2.INTER_CUBIC)
    # img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    # pytesseract.pytesseract.tesseract_cmd = 'C:/Program Files/Tesseract-OCR/tesseract.exe'
    # text = obj.text_extractor(img,3)

    
def fuzzMatch( major, minor, errs = 4, threshold = 65 ):
    """Checks if arg2 string is in arg1 string"""
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
    - Image Cleaning and Realignment is performed
    - Three configurations of pytesseract are used for OCR
    - config = 3,4,6 are used, where:
        - 3    Fully automatic page segmentation, but no OSD. (Default)
        - 4    Assume a single column of text of variable sizes.
        - 6    Assume a single uniform block of text.
        - 12   Sparse text with OSD(Orientation and script detection)

    
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
            for i in range(len(res) - 4):
                check = 1
                for j in range(3):
                    check = check and len(res[i+j]) == 4 and res[i+j].isdigit()
                # check = check and ("male" in res or "female" in res)
                if(check):
                    doctype = "Aadhaar"
        classifiedDict[doctype].append(path)
    return classifiedDict