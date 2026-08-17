from fastapi import FastAPI
app=FastAPI(
    title="Theatre Review API",
    description=(
        "A RESTful API built for a theatre booking startup that enables audiences to submit ratings and reviews for plays and performances."
         "The API powers the application's review section by allowing users to create, view, update, and manage reviews while automatically calculating average ratings for each play."
    ),
     docs_url="/docs",
        redoc_url="/redoc",
        openapi_url="/openapi.json"
    
)

   

@app.get("/")
def home():
    return {"message":"helo world"}