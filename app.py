import os
from backend import devil_advocate
from fastapi import FastAPI
from pydantic import BaseModel
import uvicorn

app = FastAPI()
devil = devil_advocate.Devil()

class TextProcessor(BaseModel):
    text: str

@app.get("/")
def read_root():
    return {"status": "running"}

@app.get("/devil")
def critique(textProcessor: TextProcessor):
    
    return {"text": '😈 '+devil.critique(textProcessor.text)+' 😈'}

if __name__ == "__main__":
    uvicorn.run("app:app", host="0.0.0.0", port=8000, reload=True)
