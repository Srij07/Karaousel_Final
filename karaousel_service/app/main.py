from fastapi import FastAPI
from dotenv import dotenv_values
from fastapi.middleware.cors import CORSMiddleware
from app.graphql.usergql import graphql_app
from app.routers.router import router as api_router

config = dotenv_values(".env")

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router)

app.include_router(graphql_app, prefix="/graphql")

@app.get("/api/health")
def root():
    return {"message": "Welcome to FastAPI with MongoDB"}