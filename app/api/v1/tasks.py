from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.schemas.task import TaskCreate, Task as TaskSchema
from app.services.task_service import TaskService

router = APIRouter(prefix="/tasks", tags=["tasks"])

@router.post("/", response_model=TaskSchema, status_code=status.HTTP_201_CREATED)
async def create_task(task_in: TaskCreate, db: Session = Depends(get_db)):
    return TaskService(db).create_task(task_in)

@router.get("/", response_model=list[TaskSchema])
async def list_tasks(db: Session = Depends(get_db)):
    return TaskService(db).list_tasks()

@router.get("/{task_id}", response_model=TaskSchema)
async def read_task(task_id: int, db: Session = Depends(get_db)):
    task = TaskService(db).get_task(task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task
