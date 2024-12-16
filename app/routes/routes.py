from fastapi import APIRouter, Form, Depends, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.database.connection import get_db
from app.models import User
from app.util.auth import get_password_hash

router = APIRouter()

templates = Jinja2Templates(directory="app/templates")

# フォームレンダリング
@router.get("/", response_class=HTMLResponse)
async def render_form(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

# フォームデータ処理
@router.post("/register")
async def register_user(
    request: Request,
    username: str = Form(...),
    email: str = Form(...),
    password: str = Form(...),
    db: AsyncSession = Depends(get_db),
):
    # ユーザー重複検査
    result = await db.execute(select(User).filter(User.username == username))
    existing_user = result.scalars().first()
    if existing_user:
        return templates.TemplateResponse(
            "index.html",
            {"request": request, "error": "存在するユーザー名です。"},
        )

    # パスワードのハッシュ後に保存
    hashed_password = get_password_hash(password)
    new_user = User(username=username, email=email, hashed_password=hashed_password)
    db.add(new_user)
    await db.commit()

    # 成功時リダイレクト
    return RedirectResponse(url="/", status_code=303)
