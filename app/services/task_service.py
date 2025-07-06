from sqlalchemy.orm import Session
from app.repositories.task_repo import TaskRepository
from app.schemas.task import TaskCreate, Task
from typing import Optional, List

class TaskService:
    def __init__(self, db: Session):
        self.repo = TaskRepository(db)

    def create_task(self, in_data: TaskCreate) -> Task:
        # place for business rules, validation, notifications, etc.
        return self.repo.create(title=in_data.title)

    def get_task(self, task_id: int) -> Optional[Task]:
        return self.repo.get(task_id)

    def list_tasks(self) -> List[Task]:
        return self.repo.list()
