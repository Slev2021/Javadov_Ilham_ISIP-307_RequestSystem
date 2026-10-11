from datetime import datetime, timedelta
from typing import List

from src.models.request import Request
from src.repository.request_repository import RequestRepository


class RequestService:
    def __init__(self, repo: RequestRepository):
        self.repo = repo

    def create_request(self, title: str, description: str,
                       author_id: int, category_id: int,
                       priority_id: int) -> Request:
        if not title or len(title.strip()) < 3:
            raise ValueError("Тема должна быть не короче 3 символов")
        if len(title) > 200:
            raise ValueError("Тема не должна превышать 200 символов")

        number = self._generate_number()
        plan_date = self._calculate_plan_date(category_id, priority_id)

        request = Request(
            id=None,
            number=number,
            title=title.strip(),
            description=description.strip(),
            author_id=author_id,
            category_id=category_id,
            status_id=1,
            priority_id=priority_id,
            plan_date=plan_date,
        )
        request_id = self.repo.create(request)
        request.id = request_id
        return request

    def get_all_requests(self) -> List[Request]:
        return self.repo.get_all()

    def get_request(self, request_id: int) -> Request:
        request = self.repo.get_by_id(request_id)
        if not request:
            raise ValueError(f"Заявка с id={request_id} не найдена")
        return request

    def update_request(self, request_id: int, title: str,
                       description: str) -> Request:
        if not title or len(title.strip()) < 3:
            raise ValueError("Тема должна быть не короче 3 символов")
        request = self.get_request(request_id)
        request.title = title.strip()
        request.description = description.strip()
        self.repo.update(request)
        return request

    def change_status(self, request_id: int, new_status_id: int) -> Request:
        request = self.get_request(request_id)

        allowed = {
            1: [2, 5],
            2: [3, 5],
            3: [4, 2],
            4: [],
            5: [],
        }
        if new_status_id not in allowed.get(request.status_id, []):
            raise ValueError(
                f"Недопустимый переход статуса: "
                f"{request.status_id} → {new_status_id}"
            )

        request.status_id = new_status_id
        if new_status_id == 4:
            request.closed_at = datetime.now()
        self.repo.update(request)
        return request

    def search(self, query: str) -> List[Request]:
        all_requests = self.repo.get_all()
        q = query.lower()
        return [
            r for r in all_requests
            if q in r.number.lower() or q in r.title.lower()
        ]

    def _generate_number(self) -> str:
        all_requests = self.repo.get_all()
        return f"REQ-{len(all_requests) + 1:04d}"

    def _calculate_plan_date(self, category_id: int,
                             priority_id: int) -> datetime:
        sla_hours = {1: 48, 2: 24, 3: 8, 4: 4}.get(category_id, 24)
        factor = {1: 1.5, 2: 1.0, 3: 0.5, 4: 0.25}.get(priority_id, 1.0)
        return datetime.now() + timedelta(hours=sla_hours * factor)