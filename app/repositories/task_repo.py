from sqlalchemy.orm import Session
from app.models.task import Task
from typing import Optional, List

class TaskRepository:
    def __init__(self, db: Session):
        self.db = db

    def get(self, task_id: int) -> Optional[Task]:
        return self.db.query(Task).filter(Task.id == task_id).first()

    def list(self) -> list[type[Task]]:
        return self.db.query(Task).all()

    def create(self, title: str) -> Task:
        db_task = Task(title=title)
        self.db.add(db_task)
        self.db.commit()
        self.db.refresh(db_task)
        return db_task
