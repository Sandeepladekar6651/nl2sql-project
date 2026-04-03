# NL2SQL API using FastAPI and Gemini

## Project Overview

This project implements a **Natural Language to SQL (NL2SQL)** system using **FastAPI and Google's Gemini LLM**.

The system allows users to ask questions in **plain English**, and the application automatically converts the question into a **SQL query**, executes it on a **SQLite database**, and returns the result.

Example:

User Question:

Show top 5 patients by spending

Generated SQL:

SELECT p.first_name, p.last_name, SUM(i.total_amount) AS total_spending
FROM patients p
JOIN invoices i ON p.id = i.patient_id
GROUP BY p.id
ORDER BY total_spending DESC
LIMIT 5;

---

# Tech Stack

Python
FastAPI
SQLite
Google Gemini LLM
Pandas

---

# Project Structure

```
nl2sql_project
│
├── main.py                # FastAPI API endpoints
├── vanna_service.py       # NL → SQL conversion service
├── setup_database.py      # Script to generate database
├── clinic.db              # SQLite database
│
├── utils/                 # Utility functions
│
├── requirements.txt       # Project dependencies
├── README.md              # Project documentation
├── .env                   # Environment variables (not committed)
```

---

# Setup Instructions

## 1 Clone the Repository

```
git clone https://github.com/Sandeepladekar6651/nl2sql-project.git
cd nl2sql-project
```

---

## 2 Install Dependencies

```
pip install -r requirements.txt
```

---

## 3 Setup Environment Variables

Create a `.env` file and add your Gemini API key.

```
GEMINI_API_KEY=your_api_key_here
```

---

## 4 Create the Database

Run the database setup script:

```
python setup_database.py
```

This will generate the SQLite database **clinic.db** with sample data.

---

## 5 Start the API Server

```
uvicorn main:app --reload
```

Server will start at:

```
http://127.0.0.1:8000
```

---

# API Documentation

Open Swagger UI:

```
http://127.0.0.1:8000/docs
```

---

# API Endpoint

## POST /chat

Convert natural language question into SQL and return results.

### Request

```
{
 "question": "Show top 5 patients by spending"
}
```

---

### Response

```
{
 "question": "Show top 5 patients by spending",
 "sql": "SELECT ...",
 "result": [...]
}
```

---

# Example Queries

You can test queries like:

Show total revenue
Show top 5 patients by spending
List all doctors
Count total appointments

---

# Features

Natural language query support
Automatic SQL generation using Gemini
SQLite database execution
FastAPI REST API
Swagger API documentation

---

# Future Improvements

Add query validation
Improve prompt engineering
Add caching for repeated queries
Support multiple databases
