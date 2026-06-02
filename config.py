import os
from dotenv import load_dotenv

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
MODEL_NAME = "gemini-1.5-flash"
MAX_TOKENS = 1024
TEMPERATURE = 0.1

DB_PATH = "data/query_history.db"

DEMO_SCHEMAS = {
    "E-Commerce": {
        "schema": """CREATE TABLE orders (
    order_id INT PRIMARY KEY,
    customer_name TEXT,
    product TEXT,
    quantity INT,
    price REAL,
    date TEXT
);
CREATE TABLE customers (
    customer_id INT PRIMARY KEY,
    name TEXT,
    email TEXT,
    city TEXT
);
CREATE TABLE products (
    product_id INT PRIMARY KEY,
    name TEXT,
    category TEXT,
    price REAL,
    stock INT
);""",
        "questions": [
            "How many orders were placed?",
            "List all products with price greater than 50",
            "What is the total revenue?",
            "Show all customers from Mumbai",
            "Which product has the highest price?"
        ]
    },
    "HR Database": {
        "schema": """CREATE TABLE employees (
    emp_id INT PRIMARY KEY,
    name TEXT,
    department TEXT,
    salary REAL,
    hire_date TEXT,
    manager_id INT
);
CREATE TABLE departments (
    dept_id INT PRIMARY KEY,
    dept_name TEXT,
    budget REAL,
    location TEXT
);""",
        "questions": [
            "What is the average salary by department?",
            "How many employees are in each department?",
            "List employees with salary greater than 50000",
            "Which department has the highest budget?",
            "Who joined after 2021?"
        ]
    },
    "Hospital": {
        "schema": """CREATE TABLE patients (
    patient_id INT PRIMARY KEY,
    name TEXT,
    age INT,
    gender TEXT,
    diagnosis TEXT,
    doctor_id INT
);
CREATE TABLE doctors (
    doctor_id INT PRIMARY KEY,
    name TEXT,
    specialty TEXT,
    experience INT
);
CREATE TABLE appointments (
    appt_id INT PRIMARY KEY,
    patient_id INT,
    doctor_id INT,
    date TEXT,
    status TEXT
);""",
        "questions": [
            "How many patients are there?",
            "List all doctors with more than 5 years experience",
            "How many appointments are scheduled?",
            "Show all patients with diabetes",
            "Which doctor has the most appointments?"
        ]
    }
}