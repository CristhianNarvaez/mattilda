from fastapi import FastAPI

from app.config import get_settings
from app.infrastructure.db.base import Base, engine

settings = get_settings()


def create_app() -> FastAPI:
    app = FastAPI(
        title=settings.PROJECT_NAME,
        version="0.1.0",
        description="Initial for FastAPI Mattilda project",
    )

    # Create database tables on startup (for dev / first run)
    @app.on_event("startup")
    def on_startup() -> None:
        Base.metadata.create_all(bind=engine)

    @app.get("/")
    def root():
        return {"message": "API is running"}

    return app


app = create_app()
