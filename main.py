from contextlib import asynccontextmanager
from pathlib import Path

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

from database import create_table
from routes.reviews import router as reviews_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    create_table()
    print("database tables created")
    yield
    print("shutting down the app")


app = FastAPI(
    title="Theatre Review API",
    description=(
        "A RESTful API built for a theatre booking startup that enables audiences to submit ratings and reviews for plays and performances. "
        "The API powers the application's review section by allowing users to create, view, update, and manage reviews while automatically calculating average ratings for each play."
    ),
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(reviews_router)


@app.get("/")
def home():
    return {"message": "Theatre Review API is running", "docs": "/docs"}


@app.get("/health")
def health_check():
    return {"status": "ok"}


@app.get("/frontend")
def serve_frontend():
    frontend_path = Path(__file__).resolve().parent / "static" / "index.html"
    return FileResponse(frontend_path)


app.mount("/static", StaticFiles(directory=str(Path(__file__).resolve().parent / "static")), name="static")
