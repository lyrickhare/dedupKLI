#Author: Raghav Rander

from fastapi import FastAPI, File, UploadFile
from fastapi.responses import FileResponse
from fastapi.responses import StreamingResponse
import train2
import json
import os
import shutil
app = FastAPI()
AADHAARIMAGEDIR_TRAIN="train/Aadhaar/"
PANIMAGEDIR_TRAIN="train/PAN/"
@app.post("/train_aadhaar")
async def upldAadhaar(files:list[UploadFile]=File(...)):
    if(os.path.exists(AADHAARIMAGEDIR_TRAIN)==False):
        os.mkdir(AADHAARIMAGEDIR_TRAIN)
    else:
        shutil.rmtree(AADHAARIMAGEDIR_TRAIN)
        os.mkdir(AADHAARIMAGEDIR_TRAIN)
    for file in files:
        contents = await file.read()
        with open(f"{AADHAARIMAGEDIR_TRAIN}{file.filename}", "wb") as f:
            f.write(contents)
    return ("uploaded Aadhaar")
@app.post("/train_pan")
async def upldPAN(files:list[UploadFile]=File(...)):
    if(os.path.exists(PANIMAGEDIR_TRAIN)==False):
        os.mkdir(PANIMAGEDIR_TRAIN)
    else:
        shutil.rmtree(PANIMAGEDIR_TRAIN)
        os.mkdir(PANIMAGEDIR_TRAIN)
    for file in files:
        contents = await file.read()
        with open(f"{PANIMAGEDIR_TRAIN}{file.filename}", "wb") as f:
            f.write(contents)
    return ("uploaded PAN")
AADHAARIMAGEDIR_VAL="validation/Aadhaar/"
PANIMAGEDIR_VAL="validation/PAN/"
@app.post("/validation_aadhaar")
async def upldAadhaar(files:list[UploadFile]=File(...)):
    if(os.path.exists(AADHAARIMAGEDIR_VAL)==False):
        os.mkdir(AADHAARIMAGEDIR_VAL)
    else:
        shutil.rmtree(AADHAARIMAGEDIR_VAL)
        os.mkdir(AADHAARIMAGEDIR_VAL)
    for file in files:
        contents = await file.read()
        with open(f"{AADHAARIMAGEDIR_VAL}{file.filename}", "wb") as f:
            f.write(contents)
    return ("uploaded Aadhaar")
@app.post("/validation_pan")
async def upldPAN(files:list[UploadFile]=File(...)):
    if(os.path.exists(PANIMAGEDIR_VAL)==False):
        os.mkdir(PANIMAGEDIR_VAL)
    else:
        shutil.rmtree(PANIMAGEDIR_VAL)
        os.mkdir(PANIMAGEDIR_VAL)
    for file in files:
        contents = await file.read()
        with open(f"{PANIMAGEDIR_VAL}{file.filename}", "wb") as f:
            f.write(contents)
    return ("uploaded PAN")
@app.get("/weights_file")
async def weightsfile():
    train2.run()
    return("your hdf5 file is ready")