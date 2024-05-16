from fastapi import APIRouter, Depends
from database import session
from sqlalchemy.orm import Session
from pydantic import BaseModel, field_validator
from typing import Annotated
from starlette import status
from models import Todos

router = APIRouter(
    prefix="/todos"
)

def get_session():
    db = session()
    try:
        yield db
    finally:
        db.close()

db_dependency = Annotated[Session, Depends(get_session)]

class CreateTodoRequest(BaseModel):
    title: str | None
    description: str | None
    priority: int | None
    completed: bool | None

    @field_validator('title')
    def title_must_be_nonempty(cls, value):
        if not value or len(value.strip()) == 0:
            raise ValueError("Title cannot be empty or whitespace.")
        return value

    @field_validator('description')
    def description_length(cls, value):
        if len(value) < 20:
            raise ValueError("Description must be at least 20 characters long.")
        return value

    @field_validator('priority')
    def priority_must_be_valid(cls, value):
        if not (1 <= value <= 5):
            raise ValueError("Priority must be between 1 and 5.")
        return value


class TodoResponse(BaseModel):
    title: str 
    description: str 
    priority: int 
    completed: bool 


@router.post("/", status_code=status.HTTP_200_OK, response_model=TodoResponse)
async def create_todo(db: db_dependency, todo_request: CreateTodoRequest):  
    todo = Todos(
        title=todo_request.title,
        description=todo_request.description,
        priority=todo_request.priority,
        completed=todo_request.completed
    )
    db.add(todo)
    db.commit()
    db.refresh(todo)  
    return todo


class GetTodoResponse(BaseModel):
    status: str
    data: list
    
@router.get("/", response_model=GetTodoResponse, status_code=status.HTTP_200_OK)
async def get_todos(db: db_dependency):
    todos = [{
        "title": i.title,
        "description": i.description,
        "priority": i.priority,
        "completed": i.completed
    } for i in db.query(Todos).all()]

    response = GetTodoResponse(
        status="success",
        data=todos
    )
    return response