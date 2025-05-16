from pydantic import BaseModel
from typing import Optional


class UpdateTaskSchema(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None