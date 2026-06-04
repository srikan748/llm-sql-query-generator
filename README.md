<div align="center">

# 🔍 SQL Query Generator

**Type a question. Get SQL. Instantly.**

[![Python](https://img.shields.io/badge/Python-3.11-blue?style=flat-square)](https://python.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-green?style=flat-square)](https://fastapi.tiangolo.com)
[![Gemini](https://img.shields.io/badge/Gemini_2.5_Flash-orange?style=flat-square)](https://ai.google.dev)
[![Live Demo](https://img.shields.io/badge/Live_Demo-HuggingFace-yellow?style=flat-square)](https://huggingface.co/spaces/ragpulse-x7/sql_query_generator)

</div>

---

## What It Does

Converts plain English into production-ready SQL using Gemini AI — similar to Amazon Q for Redshift and Google BigQuery AI.

## Results

| Metric | Value |
|---|---|
| Accuracy on Spider Benchmark | **86.7%** |
| Avg Inference Latency | **1420ms** |
| Training Samples | **7000** |
| Unit Tests | **5/5 passing** |

## Stack

`Gemini 2.5 Flash` · `FastAPI` · `Gradio` · `QLoRA` · `Docker` · `SQLite`

## Quick Start

```bash
git clone https://github.com/srikan748/llm-sql-query-generator.git
cd llm-sql-query-generator
pip install -r requirements.txt
echo "GEMINI_API_KEY=your_key" > .env
uvicorn app.api:app --port 8000    # terminal 1
python app/ui.py                   # terminal 2
```

## Docker

```bash
docker-compose up --build
```

## Live Demo

👉 [huggingface.co/spaces/ragpulse-x7/sql_query_generator](https://huggingface.co/spaces/ragpulse-x7/sql_query_generator)

---

*Built by Srikanth | Spider Dataset | Kaggle T4 GPU Training*