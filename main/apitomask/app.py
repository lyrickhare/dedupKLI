from fastapi import FastAPI, File, UploadFile
from fastapi.responses import FileResponse
# from fastapi.responses import FileResponse
import os
from random import randint
# import uuid
import shutil
from pathlib import Path
import mask
import pytesseract
IMAGEDIR = "images/"
app = FastAPI()

@app.post("/")
async def upldImg(file:UploadFile=File(...)):
    shutil.rmtree(IMAGEDIR)
    os.mkdir(IMAGEDIR)
    contents = await file.read()
    with open(f"{IMAGEDIR}{file.filename}", "wb") as f:
        f.write(contents)
    img_path = list(Path(IMAGEDIR).rglob("*")) # Input Images
    img_path_str = [str(i) for i in img_path]
    pytesseract.pytesseract.tesseract_cmd = "C:/Program Files/Tesseract-OCR/tesseract.exe"

    obj = mask.Aadhaar_Card()
    aadhaar_list = (obj.extract(img_path_str[0]))
    aadharnum = [aadhaar_list[0][:-4]]
    # splittxt = img_path_str[0].split(".")
    flag = obj.mask_image(img_path_str[0],img_path_str[0] ,aadharnum ) #supported types (png, jpeg, jpg)
    return "masked"
    # return aadhaar_list[0]
    # return FileResponse(img_path_str[0])
@app.get("/")
async def getimage():
    img_path = list(Path(IMAGEDIR).rglob("*")) # Input Images
    img_path_str = [str(i) for i in img_path]   
    return FileResponse(img_path_str[0])

#     # return "done uploading"

# @app.get("/image")
# async def dwnldImg():
#     img_path = list(Path(IMAGEDIR).rglob("*")) # Input Images
#     img_path_str = [str(i) for i in img_path]
#     obj = mask.Aadhaar_Card()
#     aadhaar_list = (obj.extract(img_path_str[0]))
#     # splittxt = img_path_str[0].split(".")
#     # flag = obj.mask_image(img_path_str[0],img_path_str[0] , aadhaar_list) #supported types (png, jpeg, jpg)
#     return aadhaar_list[0]

#     # return FileResponse("images/responseimg.jpg")
#     return FileResponse(img_path_str[0])
#     # return FileResponse("C:/Users/lyric/Desktop/primary/kotak/git/dedupKLI/lyric/test0/images/testingapiaadharRR.png")

