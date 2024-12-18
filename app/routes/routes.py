from fastapi import APIRouter, Request, Form, Depends, HTTPException
from fastapi.responses import RedirectResponse, HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from datetime import date
from app.database.connection import get_db
from app.models.models import User, Task
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
async def get_tasks(request: Request, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Task))
    tasks = result.scalars().all()
    return templates.TemplateResponse("task.html", {"request": request, "tasks": tasks})

# Task 追加ページ (GET)
@router.get("/task/add", response_class=HTMLResponse)
async def render_add_task_page(request: Request):
    return templates.TemplateResponse("addTask.html", {"request": request})

# Task 修正ページ (GET)
@router.get("/task/update/{task_id}", response_class=HTMLResponse)
async def render_update_task_page(task_id: int, request: Request, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Task).where(Task.id == task_id))
    task = result.scalars().first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return templates.TemplateResponse(
        "updateTask.html", 
        {"request": request, "task": task}
    )

@router.post("/task/add")
async def add_task(
    status: str = Form(...),
    task_name: str = Form(...),
    due_date: str = Form(...),
    task_content: str = Form(None),
    remarks: str = Form(None),
    db: AsyncSession = Depends(get_db),
):
    new_task = Task(
        status=status,
        task_name=task_name,
        due_date=date.fromisoformat(due_date),
        task_content=task_content,
        remarks=remarks,
    )
    db.add(new_task)
    await db.commit()
    # 追加後に task ページにリダイレクト
    return RedirectResponse(url="/task", status_code=303)

# タスク修正
@router.post("/task/update/{task_id}")
async def update_task(
    task_id: int,
    status: str = Form(None),
    task_name: str = Form(None),
    due_date: str = Form(None),
    task_content: str = Form(None),
    remarks: str = Form(None),
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(select(Task).where(Task.id == task_id))
    task = result.scalars().first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    
    if status:
        task.status = status
    if task_name:
        task.task_name = task_name
    if due_date:
        task.due_date = date.fromisoformat(due_date)
    if task_content:
        task.task_content = task_content
    if remarks:
        task.remarks = remarks

    await db.commit()
    return RedirectResponse(url="/task", status_code=303)

# タスク削除
@router.post("/task/delete/{task_id}")
async def delete_task(task_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Task).where(Task.id == task_id))
    task = result.scalars().first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    await db.delete(task)
    await db.commit()
    return RedirectResponse(url="/task", status_code=303)