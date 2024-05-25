# アプリのエントリーポイント
from fastapi import FastAPI
app = FastAPI()

@app.get("/")
async def hello():
    # ブラケット
    return {"hello":"hello world"}

