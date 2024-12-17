from pydantic import BaseModel

# ユーザー生成
class UserCreate(BaseModel):
    username: str
    email: str
    password: str

# ログインリクエスト
class UserLogin(BaseModel):
    username: str
    password: str

# JWT トークン
class Token(BaseModel):
    access_token: str
    token_type: str

# ユーザー情報
class Token(BaseModel):
    access_token: str
    token_type: str