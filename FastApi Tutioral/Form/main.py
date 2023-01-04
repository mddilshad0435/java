from fastapi import FastAPI, Form

app = FastAPI()

@app.post('/language/')
async def language(name:str = Form(...), type: str = Form(...)):
    return {"name": name, "type": type}