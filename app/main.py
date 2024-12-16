from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from app.database.connection import engine, Base
from app.routes.routes import router
import os

# load_dotenv()

app = FastAPI()

# @app.get("/")
# async def root():
#     env = os.getenv("APP_ENV", "unknown")
#     return {"message": f"Running in {env} environment"}

templates = Jinja2Templates(directory="app/templates")

# データベース初期化イベント
@app.on_event("startup")
async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    print("Database and tables created successfully!")

# ルートパス
@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

# ラウターの追加
app.include_router(router)