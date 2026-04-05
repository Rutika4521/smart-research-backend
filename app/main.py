from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.routes import router

app = FastAPI(title="Smart Research System")

# CORS CONFIGURATION
origins = [
    "http://localhost:5173",      # local React
    "http://127.0.0.1:5173",
    "*"                           # allow all (safe for academic project)
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router)

@app.get("/")
def root():
    return {"status": "API Running"}
