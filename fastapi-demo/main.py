from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()
users = []

class User(BaseModel):
    name: str
    age: int

@app.get("/")
def home():
    return {"message": "Hello FastAPI! Hello World"}
@app.get("/about")
def about():
    return {"app": "FastAPI Demo"}
@app.get("/users/{id}")
def get_user(id: int):
    return {"user_id": id}
@app.get("/search")
def search(name: str):
    return {"search": name}

@app.get("/users")
def get_users():
    return users

@app.post("/users")
def create_user(user: User):
    return {
        "message": "User created",
        "user": user
    }

@app.get("/users/{index}")
def get_user(index: int):
    return users[index]