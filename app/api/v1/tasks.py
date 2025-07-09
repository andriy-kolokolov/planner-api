# app/api/v1/tasks.py
from fastapi import APIRouter
from fastapi import HTTPException, status, Depends
from fastapi_utils.cbv import cbv

from app.schemas.task import TaskCreate, TaskRead
from app.schemas.user import UserRead
from app.services.auth_service import get_auth_service
from app.services.task_service import TaskService, get_task_service

router = APIRouter(prefix="/tasks", tags=["tasks"])


@cbv(router)
class Tasks:
    service: TaskService = Depends(get_task_service)

    @router.get("/", response_model=list[TaskRead])
    def list(self):
        return self.service.list_tasks()

    @router.get("/{task_id}", response_model=TaskRead)
    def read(self, task_id: int):
        task = self.service.get_task(task_id)
        if not task:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Task with id {task_id} not found",
            )
        return task

    @router.post("/", response_model=TaskRead, status_code=status.HTTP_201_CREATED)
    def create(self, task_in: TaskCreate):
        return self.service.create_task(task_in)
