from fastapi import FastAPI

app = FastAPI()

@app.get("/12")
def root():
    return {"message": "Hello World"}