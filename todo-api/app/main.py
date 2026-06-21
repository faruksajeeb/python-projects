from fastapi import FastAPI

from app.database import engine, Base
from app.routers.todo import router as todo_router

from app.models import todo  # IMPORTANT: register model

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Todo API")

@app.get("/")
def home():
    return "Hello World";
app.include_router(todo_router)
