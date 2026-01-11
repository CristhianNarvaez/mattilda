from fastapi import FastAPI


def create_app() -> FastAPI:
    app = FastAPI(
        title="Mattilda Backend Test",
        version="0.1.0",
        description="Initial bootstrap for hexagonal FastAPI project",
    )

    @app.get("/")
    def root():
        return {"message": "API is running"}

    return app


app = create_app()
