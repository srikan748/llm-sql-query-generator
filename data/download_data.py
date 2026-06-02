import json
import os
from datasets import load_dataset

print("Downloading Spider dataset...")

os.makedirs("data", exist_ok=True)

dataset = load_dataset("xlangai/spider")

train_data = []
for item in dataset["train"]:
    train_data.append({
        "question": item["question"],
        "query": item["query"],
        "db_id": item["db_id"]
    })

dev_data = []
for item in dataset["validation"]:
    dev_data.append({
        "question": item["question"],
        "query": item["query"],
        "db_id": item["db_id"]
    })

with open("data/train_spider.json", "w") as f:
    json.dump(train_data, f, indent=2)

with open("data/dev.json", "w") as f:
    json.dump(dev_data, f, indent=2)

print(f"Train samples: {len(train_data)}")
print(f"Dev samples:   {len(dev_data)}")
print(f"\nExample:")
print(f"  Question: {train_data[0]['question']}")
print(f"  SQL:      {train_data[0]['query']}")
print("Dataset ready!")