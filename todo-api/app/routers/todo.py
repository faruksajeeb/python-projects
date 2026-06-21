from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.todo import TodoCreate, TodoUpdate, TodoResponse
from app.services import todo_service

from app.auth.dependencies import get_current_user
from app.models.user import User

router = APIRouter(prefix="/todos", tags=["Todos"])

@router.post("/", response_model=TodoResponse)
def create(
    todo: TodoCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return todo_service.create_todo(db, todo, current_user.id)

@router.get("/", response_model=list[TodoResponse])
def get_all(
    skip: int = 0,
    limit: int = 10,
    search: str | None = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return todo_service.get_todos(db, current_user.id, skip, limit, search)

@router.get("/{todo_id}", response_model=TodoResponse)
def get_one(
    todo_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    todo = todo_service.get_todo(db, todo_id, current_user.id)

    if not todo:
        raise HTTPException(status_code=404, detail="Todo not found")

    return todo

@router.put("/{todo_id}", response_model=TodoResponse)
def update(
    todo_id: int,
    data: TodoUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    todo = todo_service.update_todo(db, todo_id, current_user.id, data)

    if not todo:
        raise HTTPException(status_code=404, detail="Todo not found")

    return todo

@router.delete("/{todo_id}")
def delete(
    todo_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    result = todo_service.delete_todo(db, todo_id, current_user.id)

    if not result:
        raise HTTPException(status_code=404, detail="Todo not found")

    return {"message": "Deleted successfully"}