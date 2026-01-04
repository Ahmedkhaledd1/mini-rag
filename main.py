from fastapi import FastAPI

app = FastAPI()
@app.get("/welcome")
def welcome():
    return {"message": "Welcome to the FastAPI application!"}

@app.get("/status")
def status():   
    return {"status": "Application is running smoothly."}