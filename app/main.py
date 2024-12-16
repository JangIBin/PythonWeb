from fastapi import FastAPI
from dotenv import load_dotenv
import os

load_dotenv()

app = FastAPI()

@app.get("/")
async def root():
    env = os.getenv("APP_ENV", "unknown")
    return {"message": f"Running in {env} environment"}