from pydantic import BaseModel, Field


class TodoCreate(BaseModel):
    title: str = Field(min_length=3, max_length=100)
    description: str | None = None


class TodoUpdate(BaseModel):
    title: str = Field(min_length=3, max_length=100)
    description: str | None = None
    is_completed: bool


class TodoResponse(BaseModel):
    id: int
    title: str
    description: str | None
    is_completed: bool

    model_config = {
        "from_attributes": True
    }