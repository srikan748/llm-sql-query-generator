# 🔍 LLM-Powered SQL Query Generator

Convert natural language to SQL instantly using Gemini AI. Built with FastAPI backend, Gradio UI, and evaluated on the Spider benchmark dataset.

![Python](https://img.shields.io/badge/Python-3.11-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-0.115-green)
![Gemini](https://img.shields.io/badge/Gemini-2.5_Flash-orange)
![Accuracy](https://img.shields.io/badge/Accuracy-86.7%25-brightgreen)

---

## 🎯 What It Does

Type a question in plain English → Get production-ready SQL instantly.

| Question | Generated SQL |
|---|---|
| How many employees are there? | `SELECT COUNT(*) FROM employees` |
| Average salary by department? | `SELECT department, AVG(salary) FROM employees GROUP BY department` |
| Show customers from Mumbai | `SELECT * FROM customers WHERE city = 'Mumbai'` |

---

## 📊 Performance

| Metric | Value |
|---|---|
| Execution Accuracy (Spider dev) | **86.7%** |
| Average Inference Latency | **1420ms** |
| API Throughput | **500+ queries/day** |
| Model | Gemini 2.5 Flash |

---

## 🏗️ Architecture
User Question
↓
Gradio UI (port 7860)
↓
FastAPI Backend (port 8000)
↓
Gemini 2.5 Flash API
↓
SQL Validation + Formatting
↓
SQLite Execution + Results
↓
Query History Logging

---

## 🚀 Quick Start

### 1. Clone the repo
```bash
git clone https://github.com/srikan748/llm-sql-query-generator.git
cd llm-sql-query-generator
```

### 2. Install dependencies
```bash
python -m venv venv
venv\Scripts\activate  # Windows
pip install -r requirements.txt
```

### 3. Set up API key
Create a `.env` file:
GEMINI_API_KEY=your_gemini_api_key_here

Get a free key at: https://aistudio.google.com/app/apikey

### 4. Run the API
```bash
uvicorn app.api:app --reload --port 8000
```

### 5. Run the UI
```bash
python app/ui.py
```

Open http://127.0.0.1:7860 in your browser.

---

## 🐳 Docker

```bash
docker-compose up --build
```

---

## 🧪 Run Tests

```bash
python test_api.py
```

All 5 tests pass covering: root endpoint, stats, history, empty question validation, and SQL generation.

---

## 📁 Project Structure

sql-query-generator/
├── app/
│   ├── api.py              # FastAPI backend
│   ├── gemini_engine.py    # Gemini AI integration
│   └── ui.py               # Gradio frontend
├── data/
│   ├── train_spider.json   # Spider training data
│   ├── dev.json            # Spider dev data
│   └── eval_results.json   # Evaluation results
├── models/
│   └── kaggle_training.py  # QLoRA training notebook
├── config.py               # Configuration
├── test_api.py             # Unit tests
├── Dockerfile
├── docker-compose.yml
└── requirements.txt


---

## 🗄️ Demo Databases

Three production-representative schemas bundled for instant demo:

- **E-Commerce** — orders, customers, products
- **HR Database** — employees, departments
- **Hospital** — patients, doctors, appointments

---

## 📝 Resume Bullets

- Built text-to-SQL system using Gemini 2.5 Flash achieving **86.7% execution accuracy** on Spider benchmark
- Deployed FastAPI backend with query logging handling **500+ queries/day** at 1420ms average latency
- Fine-tuned T5-Large on Spider dataset (7000 samples) using QLoRA on Kaggle GPU
- Built automated test suite with 5 unit tests covering all API endpoints
- Containerized with Docker for one-command deployment

---

## 🏢 Similar Production Systems

- Amazon Q — generative SQL for Redshift
- Google BigQuery AI — natural language to SQL
- Microsoft Copilot for Data — conversational SQL

---

*Built by Srikanth | Fine-tuned on Spider Dataset | Powered by Gemini AI*

