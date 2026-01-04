from fastapi import FastAPI,APIRouter
import os

base_router = APIRouter(
    prefix="/api/v1",
)
app_version = os.getenv("APP_VERSION")
app_name = os.getenv("APP_NAME")    
@base_router.get("/")
async def welcome():
    return {"message": "Welcome to the FastAPI application!",
            "app_name": app_name,
            "app_version": app_version}