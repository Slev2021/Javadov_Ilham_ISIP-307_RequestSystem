from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware

from src.api.routes import router
from src.api.errors import (
    AppException, app_exception_handler, validation_exception_handler,
)


app = FastAPI(
    title="RequestSystem API",
    description="REST API для системы обработки заявок",
    version="1.0.0",
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


@app.get("/", tags=["Health"])
def root():
    return {"status": "ok", "service": "RequestSystem API"}