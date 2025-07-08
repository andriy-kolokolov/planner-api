from fastapi.params import Depends
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.repositories.task_repository import TaskRepository
from app.schemas.task import TaskCreate, TaskRead
from typing import Optional, List

from app.schemas.user import UserRead


class TaskService:
    def __init__(self, db: Session):
        self.repo = TaskRepository(db)

    def create_task(self, in_data: TaskCreate) -> TaskRead:
        created = self.repo.create(title=in_data.title)
        return TaskRead.model_validate(created)

    def get_task(self, task_id: int) -> Optional[TaskRead]:
        return self.repo.get(task_id)

    def list_tasks(self) -> List[TaskRead]:
        return self.repo.list()


def get_task_service(db: Session = Depends(get_db)) -> TaskService:
    return TaskService(db)
