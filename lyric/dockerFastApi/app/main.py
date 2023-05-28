# Shri Ganeshaya Namah
# @author lyrickhare


from fastapi import FastAPI, File, UploadFile, Form

import os
import shutil
from pathlib import Path
import pytesseract
import base64

import segregateNN
import bestquality
import segregateOcrConfig
import mask


IMAGEDIR = "images/"

 
app = FastAPI()


@app.post("/classifyNdeDup")
async def deDupPost(files:list[UploadFile]=File(...)):
    if(os.path.exists(IMAGEDIR)==False):
        os.mkdir(IMAGEDIR)
    else:
        shutil.rmtree(IMAGEDIR)
        os.mkdir(IMAGEDIR)
    for file in files:
        contents = await file.read()
        with open(f"{IMAGEDIR}{file.filename}", "wb") as f:
            f.write(contents)
    img_path = list(Path(IMAGEDIR).rglob("*"))
    img_path_str = [str(i) for i in img_path]
    classifiedDict = segregateNN.segregate(img_path_str)
    deDupDict = bestquality.bestquality(classifiedDict)
    shutil.rmtree('images/')
    return deDupDict



@app.post("/verify")
async def upldImg(file:UploadFile=File(...),name : str=Form(...)):
    if(os.path.exists(IMAGEDIR)==False):
        os.mkdir(IMAGEDIR)
    else:
        shutil.rmtree(IMAGEDIR)
        os.mkdir(IMAGEDIR)
    contents = await file.read()
    with open(f"{IMAGEDIR}{file.filename}", "wb") as f:
        f.write(contents)
    img_path = list(Path(IMAGEDIR).rglob("*"))
    img_path_str = [str(i) for i in img_path]
    pytesseract.pytesseract.tesseract_cmd = "/usr/bin/tesseract"#make sure to changes in path
    text = segregateOcrConfig.OCR(img_path_str[0])
    verified = segregateOcrConfig.fuzzMatch(text,name)
    shutil.rmtree(IMAGEDIR)
    if(verified):
        return "verified"
    else:
        return "fraud"    
        
@app.post("/maskAadhar")
async def upldImg(file:UploadFile=File(...)):
    if(os.path.exists(IMAGEDIR)==False):
        os.mkdir(IMAGEDIR)
    else:
        shutil.rmtree(IMAGEDIR)
        os.mkdir(IMAGEDIR)
    contents = await file.read()
    with open(f"{IMAGEDIR}{file.filename}", "wb") as f:
        f.write(contents)
    img_path = list(Path(IMAGEDIR).rglob("*"))
    img_path_str = [str(i) for i in img_path]
    pytesseract.pytesseract.tesseract_cmd = "/usr/bin/tesseract"#make sure to changes in path
    obj = mask.Aadhaar_Card()
    aadhaar_list = (obj.extract(img_path_str[0]))
    if(len(aadhaar_list)>0):
        if(len(aadhaar_list[0])>=4):
            aadharnum = [aadhaar_list[0][:-4]]
            flag = obj.mask_image(img_path_str[0],img_path_str[0] ,aadharnum ) #supported types (png, jpeg, jpg)
            with open(img_path_str[0], "rb") as image_file:
                data = base64.b64encode(image_file.read())
            
            return {"base64Img":data}
    else:
        shutil.rmtree(IMAGEDIR)
        return {"error":"aadhar number not detected"}