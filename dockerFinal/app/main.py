# Shri Ganeshaya Namah
# @author lyrickhare

#***python libraries
from fastapi import FastAPI, File, UploadFile, Form
import os
import shutil
from pathlib import Path
import pytesseract
import base64
import fitz #requires PyMuPDF and frontend modules and not fitz

#***custom python files
import segregateNN
import bestquality
import segregateOcrConfig
import mask

# Directory in which all the uploaded images will be saved
IMAGEDIR = "images/"

# Initialising instance of a fastapi app
app = FastAPI()



def pdftoimg(pdffile):
    """
    A void function that converts pdf file to png
    - Input => relative path of pdf file
    It also deletes the pdf file at its location and generates a png file with same name at the same location
    zoom increases the clarity of output image
    ***Note => It converts only the first page of the pdf 
    ***Warning => It will give a windows error {file is being used by another process} if the pdf file is opened/used in some other program; or not closed after opening
    """
    doc = fitz.open(pdffile)
    zoom = 4
    mat = fitz.Matrix(zoom, zoom)
    count = 1
    # Count variable is to get the number of pages in the pdf and then run a for loop; but we are doing it just for first page
    val = pdffile.split(".")[0]+".png"
    page = doc.load_page(0)
    pix = page.get_pixmap(matrix=mat)
    pix.save(val)
    doc.close()
    os.remove(pdffile)


# A post method that inputs list of images and outputs the dictionary of deduplicated images; for more documentation please check the individual functions used
@app.post("/classifyNdeDup")
async def deDupPost(files:list[UploadFile]=File(...)):
    if(os.path.exists(IMAGEDIR)==False):
        os.mkdir(IMAGEDIR)
    else:
        shutil.rmtree(IMAGEDIR)
        os.mkdir(IMAGEDIR)
    for file in files:
        contents = await file.read()
        filename = str(file.filename) 
        fpath = IMAGEDIR + filename
        with open(f"{IMAGEDIR}{file.filename}", "wb") as f:
            f.write(contents)
        if(filename.split(".")[1]=="pdf"):
            pdftoimg(fpath)
    img_path = list(Path(IMAGEDIR).rglob("*"))
    img_path_str = [str(i) for i in img_path]
    classifiedDict = segregateNN.segregate(img_path_str)
    deDupDict = bestquality.bestquality(classifiedDict)
    shutil.rmtree('images/')
    return deDupDict


# A post method to verify a document. It takes a single image and verification_text as input and outputs "verified" if the verification text is found the image, else reutrns "fraud"
@app.post("/verify")
async def upldImg(file:UploadFile=File(...),name : str=Form(...)):
    if(os.path.exists(IMAGEDIR)==False):
        os.mkdir(IMAGEDIR)
    else:
        shutil.rmtree(IMAGEDIR)
        os.mkdir(IMAGEDIR)
    contents = await file.read()
    filename = str(file.filename) 
    fpath = IMAGEDIR + filename
    with open(f"{IMAGEDIR}{file.filename}", "wb") as f:
        f.write(contents)
    if(filename.split(".")[1]=="pdf"):
            pdftoimg(fpath)
        
    img_path = list(Path(IMAGEDIR).rglob("*"))
    img_path_str = [str(i) for i in img_path]
    pytesseract.pytesseract.tesseract_cmd = "/usr/bin/tesseract"#"C:/Program Files/Tesseract-OCR/tesseract.exe"make sure to changes in path
    text = segregateOcrConfig.OCR(img_path_str[0])
    verified = segregateOcrConfig.fuzzMatch(text,name)
    shutil.rmtree(IMAGEDIR)
    if(verified):
        return "verified"
    else:
        return "fraud"    
        


# This post method is used to mask aadhaar_card's first 8 digits (can be changed, please check the comment below). It outputs "aadhaar not detected" if aadhaar number digits are not found
@app.post("/maskAadhar")
async def upldImg(file:UploadFile=File(...)):
    if(os.path.exists(IMAGEDIR)==False):
        os.mkdir(IMAGEDIR)
    else:
        shutil.rmtree(IMAGEDIR)
        os.mkdir(IMAGEDIR)
    contents = await file.read()
    filename = str(file.filename) 
    fpath = IMAGEDIR + filename
    with open(f"{IMAGEDIR}{file.filename}", "wb") as f:
        f.write(contents)
    if(filename.split(".")[1]=="pdf"):
        pdftoimg(fpath)
    img_path = list(Path(IMAGEDIR).rglob("*"))
    img_path_str = [str(i) for i in img_path]
    pytesseract.pytesseract.tesseract_cmd ="/usr/bin/tesseract"#"C:/Program Files/Tesseract-OCR/tesseract.exe" make sure to changes in path
    obj = mask.Aadhaar_Card()
    aadhaar_list = (obj.extract(img_path_str[0]))
    if(len(aadhaar_list)>0):
        if(len(aadhaar_list[0])>=4):
            aadharnum = [aadhaar_list[0][:-4]] # change this 4 to any number between 0 and 11 to mask desired number of digits
            flag = obj.mask_image(img_path_str[0],img_path_str[0] ,aadharnum ) #supported types (png, jpeg, jpg)
            with open(img_path_str[0], "rb") as image_file:
                data = base64.b64encode(image_file.read())
            
            return {"base64Img":data}
    else:
        shutil.rmtree(IMAGEDIR)
        return {"error":"aadhar number not detected"}