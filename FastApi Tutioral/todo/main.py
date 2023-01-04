from fastapi import FastAPI, HTTPException,Form
from pydantic import BaseModel
from typing import Optional, List

class Todo(BaseModel):
    name: str
    date: str
    description: str

app = FastAPI(title="todo app")

store_todo = []
@app.get('/')
async def home():
    return "hello world"

@app.post("/todo/")
async def create_todo(todo: Todo):
    store_todo.append(todo)
    return todo

@app.get("/todo/",response_model=List[Todo])
async def get_all_todo():
    return store_todo

@app.get("/todo/{id}")
async def get_todo(id: int):
    try:
        return store_todo[id]
    except:
        return HTTPException(status_code=404, detail="Todo not found!")

@app.put("/todo/{id}")
async def update_todo(id:int, todo: Todo):
    try:
        store_todo[id] = todo
        return store_todo[id]
    except:
        return HTTPException(status_code=404, detail="Todo not found!")

@app.delete("/todo/{id}")
async def delete_todo(id: int):
    try:
        obj = store_todo[id]
        store_todo.pop(id)
        return obj
    except:
        return HTTPException(status_code=404, detail="Todo not found!")


