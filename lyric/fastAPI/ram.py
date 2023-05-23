from fastapi import FastAPI
app = FastAPI()

@app.get("/")
def ram1():
    return{"title":"shri ganeshaya namah"}