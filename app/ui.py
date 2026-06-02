import gradio as gr
import requests
import json
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config import DEMO_SCHEMAS

API_URL = "http://127.0.0.1:8000"

def get_schema(db_choice):
    return DEMO_SCHEMAS[db_choice]["schema"]

def get_sample_questions(db_choice):
    return gr.Dropdown(choices=DEMO_SCHEMAS[db_choice]["questions"], value=None, label="💡 Sample Questions")

def fill_question(q):
    return q if q else ""

def generate_query(question, schema, db_choice):
    if not question.strip():
        return "", "❌ Please enter a question", "", "", ""
    
    try:
        response = requests.post(f"{API_URL}/api/generate", json={
            "question": question,
            "schema": schema,
            "db_name": db_choice
        })
        data = response.json()
        
        if response.status_code != 200:
            return "", f"❌ Error: {data.get('detail', 'Unknown error')}", "", "", ""
        
        sql = data["sql"]
        latency = data["latency_ms"]
        execution = data["execution"]
        
        if execution["success"] and execution["rows"]:
            cols = execution["columns"]
            rows = execution["rows"]
            header = " | ".join(cols)
            separator = "-" * len(header)
            result_rows = "\n".join([" | ".join(str(v) for v in row) for row in rows])
            result = f"{header}\n{separator}\n{result_rows}\n\n✅ {len(rows)} row(s) returned"
        elif execution["success"]:
            result = "✅ Query executed successfully. No rows returned."
        else:
            result = f"⚠️ SQL generated but execution error:\n{execution['error']}"
        
        status = f"✅ Success — {latency}ms"
        latency_badge = f"⚡ {latency}ms"
        
        # Get updated stats
        stats_resp = requests.get(f"{API_URL}/api/stats")
        stats = stats_resp.json()
        stats_text = f"📊 Total: {stats['total_queries']} | ✅ Success: {stats['success_rate']}% | ⚡ Avg: {stats['avg_latency_ms']}ms"
        
        return sql, status, result, latency_badge, stats_text
        
    except Exception as e:
        return "", f"❌ API Error: {str(e)}", "", "", ""

def get_history():
    try:
        response = requests.get(f"{API_URL}/api/history")
        history = response.json()
        if not history:
            return "No queries yet."
        lines = []
        for h in history[:10]:
            icon = "✅" if h["success"] else "❌"
            lines.append(f"{icon} [{h['timestamp']}] {h['latency_ms']}ms\nQ: {h['question']}\nSQL: {h['sql']}\n")
        return "\n".join(lines)
    except:
        return "Could not load history."

with gr.Blocks(title="🔍 SQL Query Generator", css="""
    .gradio-container { max-width: 1200px !important; }
    .stat-box { text-align: center; padding: 10px; border-radius: 8px; }
    footer { display: none !important; }
""") as demo:

    gr.Markdown("""
    # 🔍 LLM-Powered SQL Query Generator
    **Convert natural language to SQL instantly using Gemini AI**
    
    Built with: `FastAPI` · `Gemini 2.5 Flash` · `SQLite` · `Gradio` | Fine-tuned on Spider Dataset
    ---
    """)

    with gr.Row():
        stats_display = gr.Textbox(
            value="📊 Total: 0 | ✅ Success: 0% | ⚡ Avg: 0ms",
            label="Live Stats",
            interactive=False
        )

    with gr.Row():
        with gr.Column(scale=1):
            gr.Markdown("### ⚙️ Configuration")
            db_choice = gr.Dropdown(
                choices=list(DEMO_SCHEMAS.keys()),
                value="E-Commerce",
                label="🗄️ Select Demo Database"
            )
            schema_box = gr.Code(
                value=DEMO_SCHEMAS["E-Commerce"]["schema"],
                language="sql",
                label="📋 Database Schema (DDL)",
                lines=10,
                interactive=True
            )
            sample_q = gr.Dropdown(
                choices=DEMO_SCHEMAS["E-Commerce"]["questions"],
                label="💡 Sample Questions",
                interactive=True
            )
            question = gr.Textbox(
                label="❓ Your Question",
                placeholder="e.g. How many employees are in Engineering?",
                lines=3
            )
            with gr.Row():
                submit_btn = gr.Button("⚡ Generate SQL", variant="primary", scale=3)
                clear_btn = gr.Button("🗑️ Clear", scale=1)

        with gr.Column(scale=1):
            gr.Markdown("### 📊 Results")
            latency_badge = gr.Textbox(label="⚡ Latency", interactive=False, scale=1)
            status_box = gr.Textbox(label="Status", interactive=False)
            sql_output = gr.Code(label="Generated SQL", language="sql", lines=6)
            result_output = gr.Textbox(label="Query Results", lines=8, interactive=False)

    with gr.Row():
        gr.Markdown("### 📜 Query History")
    with gr.Row():
        history_btn = gr.Button("🔄 Load History")
        history_output = gr.Textbox(label="Recent Queries", lines=12, interactive=False)

    # Event handlers
    db_choice.change(fn=get_schema, inputs=db_choice, outputs=schema_box)
    db_choice.change(fn=get_sample_questions, inputs=db_choice, outputs=sample_q)
    sample_q.change(fn=fill_question, inputs=sample_q, outputs=question)
    submit_btn.click(
        fn=generate_query,
        inputs=[question, schema_box, db_choice],
        outputs=[sql_output, status_box, result_output, latency_badge, stats_display]
    )
    question.submit(
        fn=generate_query,
        inputs=[question, schema_box, db_choice],
        outputs=[sql_output, status_box, result_output, latency_badge, stats_display]
    )
    clear_btn.click(fn=lambda: ("", "", "", "", ""), outputs=[question, sql_output, status_box, result_output, latency_badge])
    history_btn.click(fn=get_history, outputs=history_output)

if __name__ == "__main__":
    demo.launch(server_port=7860)