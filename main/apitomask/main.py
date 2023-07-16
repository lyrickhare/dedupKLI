
from fastapi import FastAPI, File, UploadFile, Form

import os
import shutil
from pathlib import Path
import pytesseract
import base64


import mask


IMAGEDIR = "images/"

 
app = FastAPI()


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
    pytesseract.pytesseract.tesseract_cmd = "C:/Program Files/Tesseract-OCR/tesseract.exe"#make sure to changes in path
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