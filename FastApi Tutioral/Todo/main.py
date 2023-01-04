from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional,List

class Todo(BaseModel):
    name:str
    due_date: str
    description: str

app = FastAPI(title="Todo API")

stroe_todo = []

@app.get('/')
async def home():
    return {"Hello":"World"}

@app.post("/todo/")
async def create_todo(todo:Todo):
    stroe_todo.append(todo)
    return todo

@app.get('/todo/',response_model=List[Todo])
async def get_all_todo():
    return stroe_todo


@app.get('/todo/{id}')
async def get_todo(id:int):
    try:
        return stroe_todo[id]
    except:
        raise HTTPException(status_code=404,detail="Todo Not Found")

@app.put('/todo/{id}')
async def update_todo(id:int,todo:Todo):
    try:
        print("to be update",stroe_todo[id])
        stroe_todo[id]=todo
        return stroe_todo[id]
    except:
        raise HTTPException(status_code=404,detail="Todo Not Found")

@app.delete('/todo/{id}')
async def delete_todo(id: int):
    try:
        obj = stroe_todo[id]
        stroe_todo.pop(id)
        return obj
    except:
        raise HTTPException(status_code=404,detail="Todo Not Found")

    