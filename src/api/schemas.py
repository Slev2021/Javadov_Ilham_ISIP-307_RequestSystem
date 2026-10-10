from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field, field_validator


# ============ Запросы ============

class RequestCreate(BaseModel):
    title: str = Field(..., min_length=3, max_length=200)
    description: Optional[str] = Field(None, max_length=2000)
    author_id: int = Field(..., gt=0)
    category_id: int = Field(..., gt=0)
    priority_id: int = Field(..., gt=0)

    @field_validator("title")
    @classmethod
    def title_not_empty(cls, v: str) -> str:
        if not v.strip():
            raise ValueError("Тема не может состоять из пробелов")
        return v.strip()


class RequestUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=3, max_length=200)
    description: Optional[str] = Field(None, max_length=2000)


class StatusChange(BaseModel):
    status_id: int = Field(..., ge=1, le=5)


# ============ Ответы ============

class RequestOut(BaseModel):
    id: int
    number: str
    title: str
    description: Optional[str]
    author_id: int
    assignee_id: Optional[int]
    category_id: int
    status_id: int
    priority_id: int
    created_at: Optional[datetime]
    plan_date: Optional[datetime]
    closed_at: Optional[datetime]


class RequestListOut(BaseModel):
    total: int
    limit: int
    offset: int
    items: list[RequestOut]


class ErrorDetail(BaseModel):
    code: str
    message: str
    details: Optional[dict] = None


class ErrorResponse(BaseModel):
    error: ErrorDetail