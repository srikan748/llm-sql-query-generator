import json
import os

print("Preparing training data...")

with open("data/train_spider.json") as f:
    train = json.load(f)

with open("data/dev.json") as f:
    dev = json.load(f)

def format_sample(item):
    return {
        "instruction": "Convert the following natural language question to a SQL query.",
        "input": f"Question: {item['question']}\nDatabase: {item['db_id']}",
        "output": item["query"]
    }

train_formatted = [format_sample(item) for item in train]
dev_formatted = [format_sample(item) for item in dev]

with open("data/train_formatted.json", "w") as f:
    json.dump(train_formatted, f, indent=2)

with open("data/dev_formatted.json", "w") as f:
    json.dump(dev_formatted, f, indent=2)

print(f"Train samples formatted: {len(train_formatted)}")
print(f"Dev samples formatted:   {len(dev_formatted)}")
print("\nSample training entry:")
print(f"  Instruction: {train_formatted[0]['instruction']}")
print(f"  Input:       {train_formatted[0]['input']}")
print(f"  Output:      {train_formatted[0]['output']}")
print("\nData ready for training!")