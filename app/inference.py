import torch
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM

MODEL_NAME = "gaussalgo/T5-LM-Large-text2sql-spider"

print("Loading model...")
tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
model = AutoModelForSeq2SeqLM.from_pretrained(MODEL_NAME)
model.eval()
print("Model ready!")

def generate_sql(question, db_schema=""):
    if db_schema:
        input_text = f"Question: {question} | {db_schema}"
    else:
        input_text = question

    inputs = tokenizer(
        input_text,
        return_tensors="pt",
        truncation=True,
        max_length=256
    )

    with torch.no_grad():
        outputs = model.generate(
            **inputs,
            max_length=128,
            num_beams=4,
            early_stopping=True
        )

    sql = tokenizer.decode(outputs[0], skip_special_tokens=True)
    return sql

if __name__ == "__main__":
    print("\nTesting inference...")
    
    test_questions = [
        ("How many employees are there?", "employees(id, name, age, department, salary)"),
        ("List all products with price greater than 100", "products(id, name, price, category)"),
        ("What is the average salary by department?", "employees(id, name, department, salary)")
    ]
    
    for question, schema in test_questions:
        sql = generate_sql(question, schema)
        print(f"\nQuestion: {question}")
        print(f"Schema:   {schema}")
        print(f"SQL:      {sql}")