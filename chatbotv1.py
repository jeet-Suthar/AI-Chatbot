import re
import sqlite3
import requests

# Hugging Face API Details
HUGGINGFACE_API_KEY = "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"
MODEL_NAME = "codellama/CodeLlama-7B-Instruct"

def generate_sql(user_input):
    # Rule 1: "Show me all employees in [department]"
    if re.match(r"show me all employees in the (.*) department", user_input, re.IGNORECASE):
        department = re.search(r"in the (.*) department", user_input, re.IGNORECASE).group(1)
        return f"SELECT * FROM Employees WHERE Department = '{department}'", "employees"

    # Rule 2: "Who is the manager of [department]?"
    elif re.match(r"who is the manager of the (.*) department", user_input, re.IGNORECASE):
        department = re.search(r"of the (.*) department", user_input, re.IGNORECASE).group(1)
        return f"SELECT Manager FROM Departments WHERE Name = '{department}'", "manager"

    # Add more rules for other query types
    else:
        print("chud gye guru!!!")
        return None, None


user_input = input("E:")

sql_query, query_type = generate_sql(user_input)

if not sql_query:
    print("Sorry, I couldn't understand your query.")

try:
    conn = sqlite3.connect('company.db')
    cursor = conn.cursor()
    cursor.execute(sql_query)
    results = cursor.fetchall()

    if not results:
        print( "No results found.")

            # Format results based on query type
    if query_type == "employees":
        print("<br>".join([f"Name: {row[1]}, Department: {row[2]}" for row in results]))
    elif query_type == "manager":
        print( f"Manager: {results[0][0]}")

except sqlite3.Error as e:
    print( f"Error: {str(e)}")
