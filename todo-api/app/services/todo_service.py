from sqlalchemy.orm import Session
from app.models.todo import Todo

from app.schemas.todo import TodoCreate, TodoUpdate


def create_todo(db: Session, todo: TodoCreate, user_id: int):
    db_todo = Todo(
        **todo.model_dump(),
        user_id=user_id
    )

    db.add(db_todo)
    db.commit()
    db.refresh(db_todo)
    return db_todo


def get_todos(db: Session, user_id: int, skip: int = 0, limit: int = 10, search: str | None = None):
    query = db.query(Todo).filter(Todo.user_id == user_id)

    if search:
        query = query.filter(Todo.title.contains(search))

    return query.offset(skip).limit(limit).all()


def get_todo(db: Session, todo_id: int, user_id: int):
    return (
        db.query(Todo)
        .filter(
            Todo.id == todo_id,
            Todo.user_id == user_id
        )
        .first()
    )


def update_todo(db: Session, todo_id: int, user_id: int, data: TodoUpdate):
    todo = get_todo(db, todo_id, user_id)

    if not todo:
        return None

    todo.title = data.title
    todo.description = data.description
    todo.is_completed = data.is_completed

    db.commit()
    db.refresh(todo)
    return todo


def delete_todo(db: Session, todo_id: int, user_id: int):
    todo = get_todo(db, todo_id, user_id)

    if not todo:
        return None

    db.delete(todo)
    db.commit()
    return True