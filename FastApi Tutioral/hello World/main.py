from typing import Optional
from fastapi import FastAPI, Form

from pydantic import BaseModel
class PackageIn(BaseModel):
    secret_id:int
    name: str
    number: str
    description: Optional[str] = None
class Package(BaseModel):
    name: str
    number: str
    description: Optional[str] = None

app = FastAPI()

@app.get('/')
async def home():
    return {'hello':"world"}

@app.get('/component/{id}')  #Execute Parameter
async def get_component(id:int):
    return {"component":id}

@app.get('/component/') #query parameter
async def read_component(number: int, text: Optional[str]):
    return {"number":number, 'text':text}


#Form 
@app.post("/form/")
async def form(name: str = Form(...), id: int = Form(...)):
    return {"name":name, "id":id}

# Pydantic Base Model
# @app.post('/package/{piority}')
# async def make_package(priority: int,package: Package,value: bool):
#     return {"priority":priority,**package.dict(),"value":value}

#Response Model
@app.post('/package/}',response_model=Package,response_model_include={"description"})
async def make_package(package: PackageIn):
    return package
