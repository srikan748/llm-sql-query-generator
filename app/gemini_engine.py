from google import genai
from google.genai import types
import time
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config import GEMINI_API_KEY, TEMPERATURE

client = genai.Client(api_key=GEMINI_API_KEY)
MODEL_NAME = "gemini-2.5-flash"

def generate_sql(question: str, schema: str) -> dict:
    prompt = f"""You are an expert SQL query generator. Given a database schema and a natural language question, generate the correct SQL query.

RULES:
- Return ONLY the SQL query, nothing else
- No explanations, no markdown, no backticks
- Use proper SQL syntax
- Use table and column names exactly as defined in the schema

DATABASE SCHEMA:
{schema}

QUESTION: {question}

SQL QUERY:"""

    start_time = time.time()
    
    try:
        response = client.models.generate_content(
            model=MODEL_NAME,
            contents=prompt,
            config=types.GenerateContentConfig(
                temperature=TEMPERATURE,
                max_output_tokens=256
            )
        )
        
        latency_ms = round((time.time() - start_time) * 1000)
        sql = response.text.strip()
        sql = sql.replace("```sql", "").replace("```", "").strip()
        if sql.endswith(";"):
            sql = sql[:-1]
            
        return {
            "sql": sql,
            "latency_ms": latency_ms,
            "success": True,
            "error": None
        }
        
    except Exception as e:
        latency_ms = round((time.time() - start_time) * 1000)
        print(f"ERROR: {str(e)}")
        return {
            "sql": "",
            "latency_ms": latency_ms,
            "success": False,
            "error": str(e)
        }


if __name__ == "__main__":
    schema = """CREATE TABLE employees (
    emp_id INT PRIMARY KEY,
    name TEXT,
    department TEXT,
    salary REAL
);"""
    
    questions = [
        "How many employees are there?",
        "What is the average salary by department?",
        "List all employees with salary greater than 50000"
    ]
    
    print("Testing Gemini SQL Engine...\n")
    for q in questions:
        result = generate_sql(q, schema)
        print(f"Question: {q}")
        print(f"SQL:      {result['sql']}")
        print(f"Latency:  {result['latency_ms']}ms")
        print(f"Status:   {'✅' if result['success'] else '❌'}")
        print()