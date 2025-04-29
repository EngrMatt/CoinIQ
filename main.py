from fastapi import FastAPI
import psycopg2
import uvicorn
from dotenv import load_dotenv
import os

# 讀取 .env 檔案
load_dotenv()

app = FastAPI()

# 從環境變數讀取資料庫連線字串
DATABASE_URL = os.getenv("DATABASE_URL")

@app.get("/")
def read_root():
    return {"message": "FastAPI is running with Neon PostgreSQL"}

@app.get("/now")
def get_db_time():
    try:
        conn = psycopg2.connect(DATABASE_URL)
        cur = conn.cursor()
        cur.execute("SELECT NOW();")
        result = cur.fetchone()
        cur.close()
        conn.close()
        return {"db_time": result[0].isoformat()}
    except Exception as e:
        return {"error": str(e)}

# 若直接執行 main.py，啟動 uvicorn
if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8484, reload=True)
