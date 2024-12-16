# タスク管理アプリ
## プロジェクト概要
FastAPIとSQLiteをベースにしたタスク管理機能を提供するウェブアプリケーションです。

## 開発環境
* Python: 3.11.x
* FastAPI: ウェブフレームワーク
* SQLite: データベース
* SQLAlchemy: ORM(Object Relational Mapping)
* Uvicorn:ASGIサーバ
* Pydantic:データ検証およびスキーマ管理
* Passlib:パスワードハッシュ
* Python-Jose: JWT 인증
* Jinja2:HTMLテンプレートエンジン
* dotenv:環境変数管理

## ローカル開発環境構築
### プロジェクト複製
Gitリポジトリでプロジェクトをクローンします。
```
git clone https://github.com/JangIBin/PythonWeb.git
cd fastapi_project
```

## 仮想環境設定
Pythonの仮想環境を生成して活性化します。

#### Mac/Linux
```
python3 -m venv venv
source venv/bin/activate
```

#### Window
```
python -m venv venv
venv\Scripts\activate
```

## 必要なパッケージのインストール
プロジェクト依存性をrequirements.txtファイルを通じてインストールします。
```
pip install -r requirements.txt
```
#### requirements.txt 内容
```
fastapi
uvicorn
sqlalchemy
aiosqlite
passlib
python-jose
jinja2
python-dotenv
```

## SQLiteデータベースの初期化
FastAPIアプリを実行すると、SQLiteデータベースが自動的に生成されます。

## FastAPIサーバー実行
以下のコマンドを実行してプロジェクトを実行します。
```
uvicorn app.main:app --reload
```

## サーバー接続
ブラウザで次のURLにアクセスします。
```
基本経路: http://127.0.0.1:8000/
Docsページ: http://127.0.0.1:8000/docs
```