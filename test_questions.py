import requests
import time

API_URL = "http://127.0.0.1:8000/chat"

questions = [
"How many patients do we have?",
"List all doctors and their specializations",
"Show me appointments for last month",
"Which doctor has the most appointments?",
"What is the total revenue?",
"Show revenue by doctor",
"How many cancelled appointments last quarter?",
"Top 5 patients by spending",
"Average treatment cost by specialization",
"Show monthly appointment count for the past 6 months",
"Which city has the most patients?",
"List patients who visited more than 3 times",
"Show unpaid invoices",
"What percentage of appointments are no-shows?",
"Show the busiest day of the week for appointments",
"Revenue trend by month",
"Average appointment duration by doctor",
"List patients with overdue invoices",
"Compare revenue between departments",
"Show patient registration trend by month"
]

print("\nTesting NL2SQL API\n")

for i, question in enumerate(questions, start=1):

    print(f"\nQuestion {i}: {question}")

    response = requests.post(API_URL, json={"question": question})

    if response.status_code == 200:
        data = response.json()

        print("Generated SQL:")
        print(data["sql"])

        print("Result:")
        print(data["result"])

    else:
        print("Error:", response.text)

    # wait 10 seconds to avoid Gemini rate limit
    time.sleep(10)