from fastapi import FastAPI
from fastapi import File,UploadFile
import segregateNN
import cv2
import numpy as np
import json
app = FastAPI()

@app.post("/upload")
async def upload(files:list[UploadFile] = File(...)):
    # contents = file.file.read()
     # with open(file.filename, 'wb') as f:
     #     f.write(contents)
    pred_list=[]
    for file in files:
        image_bytes = await file.read() 
        encoded_img = np.frombuffer(image_bytes,dtype=np.uint8)
        dict_seg = segregateNN.segregate(encoded_img)
        
    return(pred_list)

    

