from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, declarative_base

DATABASE_URL = "sqlite+aiosqlite:///./app.db"

# SQLite 非同期 データベース エンジン
engine = create_async_engine(DATABASE_URL, echo=True)

# セッション作成
SessionLocal = sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)

# モデル·ベース·クラス
Base = declarative_base()

# データベースセッション依存性
async def get_db():
    async with SessionLocal() as session:
        yield session