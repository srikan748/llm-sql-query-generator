---
title: SQL Query Generator
emoji: 🔍
colorFrom: blue
colorTo: green
sdk: gradio
sdk_version: 5.9.1
app_file: app.py
pinned: false
---

<div align="center">

# 🔍 LLM-Powered SQL Query Generator

### Convert natural language to SQL instantly using Gemini AI

[![Python](https://img.shields.io/badge/Python-3.11-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.115-009688?style=for-the-badge&logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com)
[![Gradio](https://img.shields.io/badge/Gradio-5.9-FF7C00?style=for-the-badge&logo=gradio&logoColor=white)](https://gradio.app)
[![Gemini](https://img.shields.io/badge/Gemini_2.5_Flash-AI-4285F4?style=for-the-badge&logo=google&logoColor=white)](https://ai.google.dev)
[![Docker](https://img.shields.io/badge/Docker-Ready-2496ED?style=for-the-badge&logo=docker&logoColor=white)](https://docker.com)
[![License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)](LICENSE)

**[🚀 Live Demo](https://huggingface.co/spaces/ragpulse-x7/sql_query_generator) · [📖 API Docs](http://localhost:8000/docs) · [📊 Dataset](https://huggingface.co/datasets/xlangai/spider)**

</div>

---

## 📌 Overview

An end-to-end AI system that converts plain English questions into production-ready SQL queries using Google's Gemini 2.5 Flash model. Built with a FastAPI backend, Gradio frontend, and evaluated on the Spider benchmark — the industry-standard text-to-SQL dataset.

> **Similar to:** Amazon Q for Redshift · Google BigQuery AI · Microsoft Copilot for Data

---

## ✨ Demo

| Natural Language | Generated SQL | Result |
|---|---|---|
| How many orders were placed? | `SELECT COUNT(*) FROM orders` | 3 |
| Average salary by department? | `SELECT department, AVG(salary) FROM employees GROUP BY department` | Engineering: 70000, HR: 50000 |
| Show customers from Mumbai | `SELECT * FROM customers WHERE city = 'Mumbai'` | Ravi, ravi@email.com |
| List doctors with 5+ years experience | `SELECT * FROM doctors WHERE experience > 5` | Dr. Sharma, Endocrinology |

---

## 📊 Performance Metrics

<table>
<tr>
<td align="center"><b>86.7%</b><br/>Execution Accuracy<br/>(Spider Benchmark)</td>
<td align="center"><b>1420ms</b><br/>Avg Inference<br/>Latency</td>
<td align="center"><b>500+</b><br/>Queries/Day<br/>Capacity</td>
<td align="center"><b>7000</b><br/>Training<br/>Samples</td>
</tr>
</table>

---

## 🏗️ System Architecture

────────────────────────────────────────────┐
│                  User Interface              │
│         Gradio UI (port 7860)               │
└─────────────────┬───────────────────────────┘
│ HTTP Request
┌─────────────────▼───────────────────────────┐
│              FastAPI Backend                 │
│              (port 8000)                    │
│  ┌──────────┐ ┌──────────┐ ┌────────────┐  │
│  │/generate │ │/history  │ │  /stats    │  │
│  └──────────┘ └──────────┘ └────────────┘  │
└─────────────────┬───────────────────────────┘
│
┌─────────────────▼───────────────────────────┐
│           Gemini 2.5 Flash API              │
│        (Natural Language → SQL)             │
└─────────────────┬───────────────────────────┘
│
┌─────────────────▼───────────────────────────┐
│         SQL Validation + Formatting         │
│              (sqlparse)                     │
└─────────────────┬───────────────────────────┘
│
┌─────────────────▼───────────────────────────┐
│      SQLite Execution + Result Return       │
│         Query History Logging               │
└─────────────────────────────────────────────┘

---

## 🚀 Quick Start

### Prerequisites
- Python 3.11+
- Gemini API key (free at [aistudio.google.com](https://aistudio.google.com/app/apikey))

### 1. Clone & Install
```bash
git clone https://github.com/srikan748/llm-sql-query-generator.git
cd llm-sql-query-generator
python -m venv venv
venv\Scripts\activate        # Windows
# source venv/bin/activate   # Mac/Linux
pip install -r requirements.txt
```

### 2. Configure Environment
```bash
# Create .env file
echo "GEMINI_API_KEY=your_key_here" > .env
```

### 3. Run API Backend
```bash
uvicorn app.api:app --reload --port 8000
```

### 4. Run UI
```bash
python app/ui.py
```

Open **http://127.0.0.1:7860** in your browser.

---

## 🐳 Docker Deployment

```bash
# One command to run everything
docker-compose up --build
```

Services started:
- API: http://localhost:8000
- UI: http://localhost:7860
- API Docs: http://localhost:8000/docs

---

## 📡 API Reference

### POST `/api/generate`
Convert natural language to SQL.

```json
// Request
{
  "question": "How many employees are in Engineering?",
  "schema": "CREATE TABLE employees (emp_id INT, name TEXT, department TEXT, salary REAL);",
  "db_name": "HR Database"
}

// Response
{
  "sql": "SELECT COUNT(*)\nFROM employees\nWHERE department = 'Engineering'",
  "latency_ms": 1420,
  "execution": {
    "success": true,
    "columns": ["COUNT(*)"],
    "rows": [[2]]
  }
}
```

### GET `/api/history`
Returns last 50 queries with timestamps and latency.

### GET `/api/stats`
Returns total queries, success rate, and average latency.

---

## 📁 Project Structure
sql-query-generator/
├── app/
│   ├── api.py                 # FastAPI backend (4 endpoints)
│   ├── gemini_engine.py       # Gemini AI integration
│   └── ui.py                  # Gradio frontend
├── data/
│   ├── train_spider.json      # 7000 Spider training samples
│   ├── dev_formatted.json     # 1034 evaluation samples
│   └── eval_results.json      # Benchmark results
├── models/
│   ├── adapter_config.json    # LoRA adapter config
│   ├── adapter_model.safetensors  # Fine-tuned weights
│   └── kaggle_training.py     # QLoRA training script
├── app.py                     # HuggingFace Spaces entry point
├── config.py                  # Centralized configuration
├── test_api.py                # Unit tests (5 passing)
├── eval.py                    # Evaluation script
├── Dockerfile                 # Container definition
├── docker-compose.yml         # Multi-service orchestration
└── requirements.txt
---

## 🧪 Testing

```bash
python test_api.py
```
✅ test_root passed
✅ test_stats_endpoint passed
✅ test_history_endpoint passed
✅ test_generate_empty_question passed
✅ test_generate_valid_question passed
All tests passed!

---

## 🗄️ Demo Databases

Three production-representative schemas included for instant demo:

| Database | Tables | Sample Questions |
|---|---|---|
| **E-Commerce** | orders, customers, products | Revenue analysis, customer lookup |
| **HR Database** | employees, departments | Salary reports, headcount |
| **Hospital** | patients, doctors, appointments | Patient records, scheduling |

---

## 🔧 Tech Stack

| Component | Technology |
|---|---|
| LLM | Gemini 2.5 Flash |
| Fine-tuning | QLoRA (r=16) on T5-Large |
| Training Platform | Kaggle (Tesla T4 GPU) |
| Backend | FastAPI + uvicorn |
| Frontend | Gradio 5.9 |
| Database | SQLite |
| SQL Parsing | sqlparse |
| Containerization | Docker + docker-compose |
| Deployment | HuggingFace Spaces |
| Testing | pytest + httpx |

---

---

## 🏢 Industry Context

This project mirrors production systems at:
- **Amazon** — Q for Redshift (natural language to SQL in production)
- **Google** — BigQuery AI (conversational SQL queries)
- **Microsoft** — Copilot for Data (SQL generation in Power BI)

---

## 📄 License

MIT License — free to use, modify, and distribute.

---

<div align="center">

**Built by Srikanth** | Powered by Gemini AI | Fine-tuned on Spider Dataset

⭐ Star this repo if it helped you!

</div>


