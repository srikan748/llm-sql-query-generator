# ============================================
# SQL Query Generator - QLoRA Training
# Run this entire file in a Kaggle Notebook
# GPU: P100 (free) - Settings > Accelerator
# ============================================

# Step 1: Install packages
import subprocess
subprocess.run(["pip", "install", "-q", "transformers", "peft", "bitsandbytes", "accelerate", "datasets"])

# Step 2: Imports
import json
import torch
from transformers import (
    AutoTokenizer,
    AutoModelForCausalLM,
    TrainingArguments,
    Trainer,
    DataCollatorForSeq2Seq,
    BitsAndBytesConfig
)
from peft import LoraConfig, get_peft_model, TaskType
from datasets import Dataset

print("All imports done!")
print(f"GPU available: {torch.cuda.is_available()}")
if torch.cuda.is_available():
    print(f"GPU name: {torch.cuda.get_device_name(0)}")

# Step 3: Load your formatted data
# Upload train_formatted.json to Kaggle first
with open("/kaggle/input/spider-sql-data/train_formatted.json") as f:
    train_data = json.load(f)

with open("/kaggle/input/spider-sql-data/dev_formatted.json") as f:
    dev_data = json.load(f)

print(f"Train: {len(train_data)} samples")
print(f"Dev:   {len(dev_data)} samples")

# Step 4: Load tokenizer
MODEL_NAME = "codellama/CodeLlama-7b-Instruct-hf"
tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
tokenizer.pad_token = tokenizer.eos_token

# Step 5: Format prompt
def format_prompt(item):
    return f"""### Instruction:
{item['instruction']}

### Input:
{item['input']}

### Response:
{item['output']}"""

# Step 6: Tokenize
def tokenize(item):
    prompt = format_prompt(item)
    result = tokenizer(
        prompt,
        truncation=True,
        max_length=512,
        padding="max_length"
    )
    result["labels"] = result["input_ids"].copy()
    return result

train_dataset = Dataset.from_list(train_data).map(tokenize)
dev_dataset = Dataset.from_list(dev_data).map(tokenize)

print("Tokenization done!")

# Step 7: Load model with 4-bit quantization
bnb_config = BitsAndBytesConfig(
    load_in_4bit=True,
    bnb_4bit_quant_type="nf4",
    bnb_4bit_compute_dtype=torch.float16
)

model = AutoModelForCausalLM.from_pretrained(
    MODEL_NAME,
    quantization_config=bnb_config,
    device_map="auto"
)

print("Model loaded!")

# Step 8: Apply LoRA
lora_config = LoraConfig(
    task_type=TaskType.CAUSAL_LM,
    r=16,
    lora_alpha=32,
    lora_dropout=0.05,
    target_modules=["q_proj", "v_proj"]
)

model = get_peft_model(model, lora_config)
model.print_trainable_parameters()

# Step 9: Training arguments
training_args = TrainingArguments(
    output_dir="/kaggle/working/sql-qlora",
    num_train_epochs=3,
    per_device_train_batch_size=4,
    per_device_eval_batch_size=4,
    warmup_steps=100,
    logging_steps=50,
    save_steps=500,
    evaluation_strategy="steps",
    eval_steps=500,
    learning_rate=2e-4,
    fp16=True,
    report_to="none"
)

# Step 10: Train
trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=train_dataset,
    eval_dataset=dev_dataset,
    data_collator=DataCollatorForSeq2Seq(tokenizer, model=model, padding=True)
)

print("Starting training...")
trainer.train()

# Step 11: Save adapter weights only (~40MB)
model.save_pretrained("/kaggle/working/sql-lora-adapter")
tokenizer.save_pretrained("/kaggle/working/sql-lora-adapter")

print("Training complete! Adapter saved.")