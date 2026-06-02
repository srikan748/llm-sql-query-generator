from fastapi import FastAPI, HTTPException, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import sqlite3
import sqlparse
import time
import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from app.gemini_engine import generate_sql
from config import DB_PATH, DEMO_SCHEMAS

app = FastAPI(
    title="SQL Query Generator API",
    description="Convert natural language to SQL using Gemini AI",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"]
)

# Initialize history database
def init_db():
    os.makedirs("data", exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS query_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            question TEXT,
            schema TEXT,
            sql TEXT,
            latency_ms INTEGER,
            success INTEGER,
            timestamp TEXT
        )
    """)
    conn.commit()
    conn.close()

init_db()

def log_query(question, schema, sql, latency_ms, success):
    conn = sqlite3.connect(DB_PATH)
    conn.execute("""
        INSERT INTO query_history (question, schema, sql, latency_ms, success, timestamp)
        VALUES (?, ?, ?, ?, ?, datetime('now'))
    """, (question, schema, sql, latency_ms, int(success)))
    conn.commit()
    conn.close()

def execute_sql(sql: str, schema: str, db_name: str) -> dict:
    try:
        conn = sqlite3.connect(":memory:")
        cursor = conn.cursor()
        
        if db_name in DEMO_SCHEMAS:
            ddl = DEMO_SCHEMAS[db_name]["schema"]
            conn.executescript(ddl)
            
            if db_name == "E-Commerce":
                conn.executescript("""
                    INSERT INTO orders VALUES (1,'Ravi','Laptop',1,45000,'2024-01-01');
                    INSERT INTO orders VALUES (2,'Priya','Phone',2,15000,'2024-01-02');
                    INSERT INTO orders VALUES (3,'Amit','Tablet',1,25000,'2024-01-03');
                    INSERT INTO products VALUES (1,'Laptop','Electronics',45000,10);
                    INSERT INTO products VALUES (2,'Phone','Electronics',15000,25);
                    INSERT INTO products VALUES (3,'Shirt','Clothing',800,100);
                    INSERT INTO customers VALUES (1,'Ravi','ravi@email.com','Mumbai');
                    INSERT INTO customers VALUES (2,'Priya','priya@email.com','Delhi');
                """)
            elif db_name == "HR Database":
                conn.executescript("""
                    INSERT INTO employees VALUES (1,'Ravi','Engineering',75000,'2020-01-01',NULL);
                    INSERT INTO employees VALUES (2,'Priya','Engineering',65000,'2021-03-15',1);
                    INSERT INTO employees VALUES (3,'Amit','HR',55000,'2019-06-01',NULL);
                    INSERT INTO employees VALUES (4,'Sneha','HR',45000,'2022-01-10',3);
                    INSERT INTO departments VALUES (1,'Engineering',500000,'Hyderabad');
                    INSERT INTO departments VALUES (2,'HR',200000,'Bangalore');
                """)
            elif db_name == "Hospital":
                conn.executescript("""
                    INSERT INTO patients VALUES (1,'Ravi',35,'Male','Diabetes',1);
                    INSERT INTO patients VALUES (2,'Priya',28,'Female','Fever',2);
                    INSERT INTO patients VALUES (3,'Amit',45,'Male','Hypertension',1);
                    INSERT INTO doctors VALUES (1,'Dr. Sharma','Endocrinology',10);
                    INSERT INTO doctors VALUES (2,'Dr. Rao','General',3);
                    INSERT INTO appointments VALUES (1,1,1,'2024-01-01','Scheduled');
                    INSERT INTO appointments VALUES (2,2,2,'2024-01-02','Completed');
                """)

        cursor.execute(sql)
        rows = cursor.fetchall()
        columns = [d[0] for d in cursor.description] if cursor.description else []
        conn.close()
        return {"success": True, "columns": columns, "rows": rows, "error": None}
    except Exception as e:
        return {"success": False, "columns": [], "rows": [], "error": str(e)}

class QueryRequest(BaseModel):
    question: str
    schema: str
    db_name: str = "Custom"

@app.post("/api/generate")
def generate(req: QueryRequest):
    if not req.question.strip():
        raise HTTPException(status_code=400, detail="Question cannot be empty")
    
    result = generate_sql(req.question, req.schema)
    
    if not result["success"]:
        raise HTTPException(status_code=500, detail=result["error"])
    
    formatted_sql = sqlparse.format(result["sql"], reindent=True, keyword_case="upper")
    execution = execute_sql(result["sql"], req.schema, req.db_name)
    log_query(req.question, req.schema, result["sql"], result["latency_ms"], result["success"])
    
    return {
        "sql": formatted_sql,
        "raw_sql": result["sql"],
        "latency_ms": result["latency_ms"],
        "execution": execution
    }

@app.get("/api/history")
def get_history():
    conn = sqlite3.connect(DB_PATH)
    rows = conn.execute("""
        SELECT id, question, sql, latency_ms, success, timestamp
        FROM query_history ORDER BY id DESC LIMIT 50
    """).fetchall()
    conn.close()
    return [{"id": r[0], "question": r[1], "sql": r[2], "latency_ms": r[3], "success": bool(r[4]), "timestamp": r[5]} for r in rows]

@app.get("/api/stats")
def get_stats():
    conn = sqlite3.connect(DB_PATH)
    total = conn.execute("SELECT COUNT(*) FROM query_history").fetchone()[0]
    success = conn.execute("SELECT COUNT(*) FROM query_history WHERE success=1").fetchone()[0]
    avg_latency = conn.execute("SELECT AVG(latency_ms) FROM query_history WHERE success=1").fetchone()[0]
    conn.close()
    return {
        "total_queries": total,
        "successful_queries": success,
        "success_rate": round(success/total*100, 1) if total > 0 else 0,
        "avg_latency_ms": round(avg_latency) if avg_latency else 0
    }

@app.get("/")
def root():
    return {"message": "SQL Query Generator API", "version": "1.0.0", "status": "running"}