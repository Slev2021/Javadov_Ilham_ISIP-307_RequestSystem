from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass
class Request:
    id: Optional[int]
    number: str
    title: str
    description: str
    author_id: int
    category_id: int
    status_id: int
    priority_id: int
    assignee_id: Optional[int] = None
    created_at: Optional[datetime] = None
    plan_date: Optional[datetime] = None
    closed_at: Optional[datetime] = None