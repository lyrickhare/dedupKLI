from fastapi import FastAPI, File, UploadFile
# from fastapi.responses import FileResponse
import os
from random import randint
# import uuid
import segregateNN
import bestquality
import shutil
from pathlib import Path

IMAGEDIR = "images/"
 
app = FastAPI()

@app.post("/")
async def deDup1(files:list[UploadFile]=File(...)):
    os.mkdir(IMAGEDIR)

    # classifiedDict = {"PAN":[],"DL":[],"Passport":[],"Aadhaar":[],"other":[]}
    # classifiedDict = {"PAN":"","DL":"","Passport":"","Aadhaar":"","other":[]}

    fnames = []
    varPAN = 0
    varAadhar = 0
    for file in files:
        # file.filename = f"{uuid.uuid4()}.jpg"
        contents = await file.read()
        with open(f"{IMAGEDIR}{file.filename}", "wb") as f:
            f.write(contents)
        # docName = segregateNN.segregate(IMAGEDIR+str(file.filename))
        # classifiedDict[docName].append(file.filename)
        # var = bestquality.var(IMAGEDIR + str(file.filename))
        # if(docName=="PAN"):
        #     if(varPAN<var):
        #         varPAN = var
        #         classifiedDict[docName] = str(file.filename)
        # elif(docName=="Aadhaar"):
        #     if(varAadhar<var):
        #         varAadhar = var
        #         classifiedDict[docName] = str(file.filename)
        # else:
        #     classifiedDict[docName].append(file.filename)
    img_path = list(Path(IMAGEDIR).rglob("*")) # Input Images
    img_path_str = [str(i) for i in img_path]
    classifiedDict = segregateNN.segregate(img_path_str)
    deDupDict = bestquality.bestquality(classifiedDict)
    shutil.rmtree('images/')
    return deDupDict
    
        
    