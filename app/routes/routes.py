from fastapi import APIRouter, Request, Form, Depends, HTTPException
from fastapi.responses import RedirectResponse, HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.database.connection import get_db
from app.models.models import User
from app.util.auth import get_password_hash, verify_password, create_access_token

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")

# index ページ (GET)
@router.get("/", response_class=HTMLResponse)
async def render_index_page(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

# ログイン ページ (GET)
@router.get("/login", response_class=HTMLResponse)
async def render_login_page(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})

# ログイン 処理 (POST)
@router.post("/login")
async def login(
    request: Request,
    email: str = Form(...),
    password: str = Form(...),
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(select(User).filter(User.email == email))
    user = result.scalars().first()
    if not user or not verify_password(password, user.hashed_password):
        return templates.TemplateResponse(
            "login.html", {"request": request, "error": "メールまたはパスワードが無効です"}
        )
    return RedirectResponse(url="/task", status_code=303)

# アカウント登録 ページ (GET)
@router.get("/signup", response_class=HTMLResponse)
async def render_signup_page(request: Request):
    return templates.TemplateResponse("signup.html", {"request": request})

# アカウント登録 処理 (POST)
@router.post("/signup")
async def signup(
    request: Request,
    username: str = Form(...),
    email: str = Form(...),
    password: str = Form(...),
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(select(User).filter(User.email == email))
    if result.scalars().first():
        raise HTTPException(status_code=400, detail="メールアドレスが既に登録されています")
    
    hashed_password = get_password_hash(password)
    new_user = User(username=username, email=email, hashed_password=hashed_password)
    db.add(new_user)
    await db.commit()
    return RedirectResponse(url="/login", status_code=303)

# Task ページ (GET)
@router.get("/task", response_class=HTMLResponse)
async def render_task_page(request: Request):
    return templates.TemplateResponse("task.html", {"request": request})
