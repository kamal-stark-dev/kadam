from fastapi import FastAPI

app = FastAPI(title="Kadam API", version="0.1.0")


@app.get("/")
def root():
    return {"message": "Kadam API is running"}


@app.get("/health", tags=["system"])
def health_check() -> dict[str, str]:
    """Return a lightweight readiness response."""
    return {"status": "ok"}