# @author: Lyric Khare
# we will need to increase the default volume of docker container before uploading images
from fastapi import FastAPI, File, UploadFile
from fastapi.responses import FileResponse
from fastapi.responses import StreamingResponse
import train2
# import json
import os
import shutil
import fitz #requires PyMuPDF and frontend modules


app = FastAPI()
trainDir = "train"
validationDir = "validation"
docNameCodesDict = {"0":"Aadhaar","1":"PAN"}
def trainOrVal(isTrain):
    if(isTrain):
        return trainDir
    return validationDir

def pdftoimg(pdffile):
    doc = fitz.open(pdffile)
    zoom = 4
    mat = fitz.Matrix(zoom, zoom)
    count = 1
    # Count variable is to get the number of pages in the pdf
    val = pdffile.split(".")[0]+".png"
    page = doc.load_page(0)
    pix = page.get_pixmap(matrix=mat)
    pix.save(val)
    doc.close()
    os.remove(pdffile)

@app.get("/getDocNameCodes")
async def docnamecodes():
    return docNameCodesDict


@app.post("/uploadDocuments")
async def upldimgs(docNameCode : str , isTrain:bool, files:list[UploadFile]=File(...)):
    imageSavingPath = trainOrVal(isTrain)+"/"+docNameCodesDict[docNameCode]+"/"

    if(os.path.exists(trainOrVal(isTrain))==False):
        os.mkdir(trainOrVal(isTrain)+"/")
    if(os.path.exists(imageSavingPath)==False):
        os.mkdir(imageSavingPath)
    for file in files:
        contents = await file.read()
        filename = str(file.filename)  
        fpath = imageSavingPath + filename        
        with open(fpath, "wb") as f:
            f.write(contents)

        if(filename.split(".")[1]=="pdf"):
            pdftoimg(fpath)
            
        return ("uploaded images")



@app.get("/weights_file")
async def weightsfile(train_batch_size : int, validation_batch_size: int, epochno : int):
    train2.run(train_batch_size, validation_batch_size, epochno,len(docNameCodesDict))
    return("your hdf5 file is ready")


@app.get("/DeleteAllImgs")
async def delimgs():
    if(os.path.exists(trainDir)==True):
        shutil.rmtree(trainDir)
    if(os.path.exists(validationDir)==True):
        shutil.rmtree(validationDir)
    return "successfully deleted all images"