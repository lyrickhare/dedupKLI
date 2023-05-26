from fastapi import FastAPI, File, UploadFile, Form
from fastapi.responses import FileResponse
# from fastapi.responses import FileResponse
import os
from random import randint
# import uuid
import shutil
from pathlib import Path
import segregateOcrConfig
import pytesseract
IMAGEDIR = "images/"
app = FastAPI()

@app.post("/")
async def upldImg(file:UploadFile=File(...),name : str=Form(...)):

    if(os.path.exists("images/")):
        shutil.rmtree(IMAGEDIR)
    os.mkdir(IMAGEDIR)
    contents = await file.read()
    with open(f"{IMAGEDIR}{file.filename}", "wb") as f:
        f.write(contents)
    img_path = list(Path(IMAGEDIR).rglob("*")) # Input Images
    img_path_str = [str(i) for i in img_path]
    pytesseract.pytesseract.tesseract_cmd = "../Tesseract-OCR/tesseract.exe"
    text = segregateOcrConfig.OCR(img_path_str[0])
    verified = segregateOcrConfig.fuzzMatch(text,name)
    # return verified
    if(verified):
        return "verified"
    else:
        return "fraud"

    # obj = mask.Aadhaar_Card()
    # aadhaar_list = (obj.extract(img_path_str[0]))
    # aadharnum = [aadhaar_list[0][:-4]]
    # # splittxt = img_path_str[0].split(".")
    # flag = obj.mask_image(img_path_str[0],img_path_str[0] ,aadharnum ) #supported types (png, jpeg, jpg)
    # # return aadhaar_list[0]
    # return FileResponse(img_path_str[0])