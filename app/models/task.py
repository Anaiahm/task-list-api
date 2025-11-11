from sqlalchemy.orm import Mapped, mapped_column
from ..db import db
from datetime import datetime

class Task(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    title: Mapped[str] = mapped_column(nullable=False)
    description: Mapped[str] = mapped_column(nullable=False)
    completed_at: Mapped[datetime] = mapped_column(default=None, nullable=True)


    def to_dict(Task):

        return {
            "id": Task.id,
            "title": Task.title,
            "description": Task.description,
            "is_complete": Task.completed_at is not None
        }
    
    def from_dict(dict):
        title = dict["title"]
        description = dict["description"]
        completed_at = None
        return Task(title=title, description=description, completed_at=completed_at)
    
