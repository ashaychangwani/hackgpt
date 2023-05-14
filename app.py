import os
from backend import devil_advocate, fact_check, assisstant, grammar, tone, beautify
from fastapi import FastAPI
from pydantic import BaseModel
import uvicorn

app = FastAPI()
devil = devil_advocate.Devil()
factChecker = fact_check.FactChecker()
assisstant = assisstant.Assisstant()
grammar = grammar.Grammar()
tone = tone.Tone()
beautify = beautify.Beautify()

class TextProcessor(BaseModel):
    text: str

class TextFixer(TextProcessor):
    critique: str

class TextQuery(TextProcessor):
    query: str

@app.get("/")
def read_root():
    return {"status": "running"}

@app.get("/devil")
def critique(textProcessor: TextProcessor):
    return {"text": '😈 '+devil.critique(textProcessor.text)+' 😈'}

@app.get("/fix")
def fix(textFixer: TextFixer):
    return {"text": devil.fix(textFixer.text, textFixer.critique)} 

@app.get("/fact-check")
def check(textProcessor: TextProcessor):
    return {"text": '🔍 '+factChecker.check(textProcessor.text)+' 🔍'}

@app.get("/assisstant")
def query(textQuery: TextQuery):
    #save the text to a file
    with open("tmp/essay.txt", "w") as f:
        f.write(textQuery.text)
    return {"text": '🤖 '+assisstant.help('tmp/essay.txt', textQuery.query)+' 🤖'}

@app.get("/grammar")
def check(textProcessor: TextProcessor):
    return {"text": grammar.fix(textProcessor.text)}

@app.get("/tone")
def check(textFixer: TextFixer):
    return {"text": tone.fix(textFixer.text, textFixer.critique)}
    
@app.get("/beautify")
def check(textFixer: TextProcessor):
    return {"text": beautify.fix(textFixer.text)}
    
if __name__ == "__main__":
    uvicorn.run("app:app", host="0.0.0.0", port=8000, reload=True, reload_excludes='frontend/*')
