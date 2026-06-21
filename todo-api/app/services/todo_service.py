from sqlalchemy.orm import Session
from app.models.todo import Todo
from app.schemas.todo import TodoCreate, TodoUpdate


def create_todo(db: Session, todo: TodoCreate):
    db_todo = Todo(**todo.model_dump())
    db.add(db_todo)
    db.commit()
    db.refresh(db_todo)
    return db_todo


def get_todos(db: Session, skip: int = 0, limit: int = 10, search: str | None = None):
    query = db.query(Todo)

    if search:
        query = query.filter(Todo.title.contains(search))

    return query.offset(skip).limit(limit).all()


def get_todo(db: Session, todo_id: int):
    return db.query(Todo).filter(Todo.id == todo_id).first()


def update_todo(db: Session, todo_id: int, data: TodoUpdate):
    todo = get_todo(db, todo_id)

    if not todo:
        return None

    todo.title = data.title
    todo.description = data.description
    todo.is_completed = data.is_completed

    db.commit()
    db.refresh(todo)
    return todo


def delete_todo(db: Session, todo_id: int):
    todo = get_todo(db, todo_id)

    if not todo:
        return None

    db.delete(todo)
    db.commit()
    return True