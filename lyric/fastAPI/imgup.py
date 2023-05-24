from fastapi import FastAPI, File, UploadFile

app = FastAPI()


@app.post("/")
async def UploadImage(file: bytes = File(...),fname: str | None = None):
    with open(fname+'.jpg','wb') as image:
        image.write(file)
        image.close()
    return 'got it'