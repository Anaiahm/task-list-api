from sqlalchemy.orm import Mapped, mapped_column
from ..db import db
from datetime import datetime

class Task(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    title: Mapped[str] = mapped_column(nullable=False)
    description: Mapped[str] = mapped_column(nullable=False)
    completed_at: Mapped[datetime] = mapped_column(default=None, nullable=True)
    # is_complete: Mapped[bool] = mapped_column(default=False, nullable=False)

    def to_dict(Task):

        return {
            "id": Task.id,
            "title": Task.title,
            "description": Task.description,
            # "completed_at": Task.completed_at,
            "completed_at": None,
            # "is_complete": Task.is_complete
        }
    
    def from_dict(dict):
        # id = dict["id"]
        title = dict["title"]
        description = dict["description"]
        # completed_at = dict["completed_at"]
        completed_at = None
        return Task(title=title, description=description, completed_at=completed_at)
    
