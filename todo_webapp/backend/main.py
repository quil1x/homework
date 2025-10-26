from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Dict

class Todo(BaseModel):
    id: int
    title: str
    is_done: bool = False

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

db: Dict[int, Todo] = {}
id_counter = 0

@app.get("/todos/", response_model=List[Todo])
async def get_all_todos():
    return list(db.values())

@app.post("/todos/", response_model=Todo)
async def create_todo(title_body: dict):
    global id_counter
    id_counter += 1
    todo = Todo(id=id_counter, title=title_body["title"])
    db[id_counter] = todo
    return todo

@app.put("/todos/{todo_id}", response_model=Todo)
async def update_todo_status(todo_id: int, status_body: dict):
    todo = db[todo_id]
    todo.is_done = status_body["is_done"]
    return todo

@app.delete("/todos/{todo_id}", status_code=204)
async def delete_todo(todo_id: int):
    del db[todo_id]
    return


#uvicorn main:app --host 0.0.0.0 --port 8000