from datetime import datetime

from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware

from src.api.routes import router
from src.api.errors import (
    AppException, app_exception_handler, validation_exception_handler,
)

from src.config.settings import settings

app = FastAPI(
    title=settings.API_TITLE,
    version=settings.API_VERSION,
    debug=settings.DEBUG,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.add_exception_handler(AppException, app_exception_handler)
app.add_exception_handler(RequestValidationError, validation_exception_handler)

app.include_router(router)


@app.get("/health", tags=["Health"])
def health_check():
    """Проверка работоспособности приложения."""
    return {
        "status": "ok",
        "service": "RequestSystem API",
        "version": settings.API_VERSION,
        "timestamp": datetime.now().isoformat(),
    }


@app.get("/", tags=["Health"])
def root():
    return {"status": "ok"}