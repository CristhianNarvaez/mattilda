from fastapi import FastAPI

from app.config import get_settings
from app.api.v1 import students_router, invoices_router
from app.infrastructure.db.base import Base, engine

settings = get_settings()


def create_app() -> FastAPI:
    app = FastAPI(
        title=settings.PROJECT_NAME,
        version="0.1.0",
        description="Hexagonal FastAPI project for Mattilda test",
    )

    @app.on_event("startup")
    def on_startup() -> None:
        Base.metadata.create_all(bind=engine)

    @app.get("/")
    def root():
        return {"message": "API is running"}

    # Register routers under /api/v1
    app.include_router(
        students_router,
        prefix=settings.API_V1_PREFIX,
    )
    app.include_router(
        invoices_router,
        prefix=settings.API_V1_PREFIX,
    )

    return app


app = create_app()
