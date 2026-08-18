from contextlib import asynccontextmanager
from fastapi import FastAPI
from database import create_table



@asynccontextmanager
async def lifespan(app:FastAPI):
    create_table()
    print("database tables created")
    yield
    print("shutting down the app")


app=FastAPI(
    title="Theatre Review API",
    description=(
        "A RESTful API built for a theatre booking startup that enables audiences to submit ratings and reviews for plays and performances."
         "The API powers the application's review section by allowing users to create, view, update, and manage reviews while automatically calculating average ratings for each play."
    ),
     docs_url="/docs",
        redoc_url="/redoc",
        openapi_url="/openapi.json",
    lifespan=lifespan
)

   

@app.get("/")
def home():
    return {"message":"helo world"}