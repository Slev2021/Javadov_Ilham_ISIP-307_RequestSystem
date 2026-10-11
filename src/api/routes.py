from fastapi import APIRouter, Query, Depends

from src.api.schemas import (
    RequestCreate, RequestUpdate, StatusChange,
    RequestOut, RequestListOut,
)
from src.api.errors import AppException
from src.service.request_service import RequestService
from src.repository.request_repository import RequestRepository


router = APIRouter(prefix="/api/requests", tags=["Requests"])


def get_service() -> RequestService:
    return RequestService(RequestRepository())


# ============ Создание ============

@router.post("", response_model=RequestOut, status_code=201)
def create_request(payload: RequestCreate,
                   service: RequestService = Depends(get_service)):
    try:
        request = service.create_request(
            title=payload.title,
            description=payload.description or "",
            author_id=payload.author_id,
            category_id=payload.category_id,
            priority_id=payload.priority_id,
        )
        return request
    except ValueError as e:
        raise AppException("VALIDATION_ERROR", str(e), 422)


# ============ Список + фильтры ============

@router.get("", response_model=RequestListOut)
def list_requests(
    status_id: int | None = Query(None, gt=0),
    category_id: int | None = Query(None, gt=0),
    priority_id: int | None = Query(None, gt=0),
    q: str | None = Query(None, max_length=100),
    limit: int = Query(10, ge=1, le=100),
    offset: int = Query(0, ge=0),
    service: RequestService = Depends(get_service),
):
    items = service.get_all_requests()

    if status_id is not None:
        items = [r for r in items if r.status_id == status_id]
    if category_id is not None:
        items = [r for r in items if r.category_id == category_id]
    if priority_id is not None:
        items = [r for r in items if r.priority_id == priority_id]
    if q:
        q_lower = q.lower()
        items = [
            r for r in items
            if q_lower in r.title.lower() or q_lower in r.number.lower()
        ]

    total = len(items)
    items = items[offset:offset + limit]

    return {"total": total, "limit": limit, "offset": offset, "items": items}


# ============ Получение одной ============

@router.get("/{request_id}", response_model=RequestOut)
def get_request(request_id: int,
                service: RequestService = Depends(get_service)):
    try:
        return service.get_request(request_id)
    except ValueError as e:
        raise AppException("NOT_FOUND", str(e), 404)


# ============ Обновление ============

@router.put("/{request_id}", response_model=RequestOut)
def update_request(request_id: int, payload: RequestUpdate,
                   service: RequestService = Depends(get_service)):
    try:
        current = service.get_request(request_id)
        title = payload.title if payload.title else current.title
        description = (payload.description
                       if payload.description is not None
                       else current.description)
        return service.update_request(request_id, title, description)
    except ValueError as e:
        raise AppException("VALIDATION_ERROR", str(e), 422)


# ============ Смена статуса ============

@router.patch("/{request_id}/status", response_model=RequestOut)
def change_status(request_id: int, payload: StatusChange,
                  service: RequestService = Depends(get_service)):
    try:
        return service.change_status(request_id, payload.status_id)
    except ValueError as e:
        message = str(e)
        if "не найдена" in message:
            raise AppException("NOT_FOUND", message, 404)
        raise AppException("INVALID_TRANSITION", message, 422)


# ============ Удаление ============

@router.delete("/{request_id}", status_code=204)
def delete_request(request_id: int,
                   service: RequestService = Depends(get_service)):
    try:
        service.get_request(request_id)  # проверка существования
        service.repo.delete(request_id)
        return None
    except ValueError as e:
        raise AppException("NOT_FOUND", str(e), 404)