import os
os.environ["GRPC_ENABLE_FORK_SUPPORT"] = "0"  # Fix gRPC shutdown warnings
os.environ["TF_CPP_MIN_LOG_LEVEL"] = "2"  # Suppress TensorFlow logs
import re
import sqlite3
import requests
import json
import google.generativeai as genai


# Hugging Face API Details
# HUGGINGFACE_API_KEY = "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"
# MODEL_NAME = "deepseek-ai/DeepSeek-R1"  # Smaller model that works for SQL

# Set up Gemini API Key
genai.configure(api_key="AIzaSyCC6iznCyPjfZjRHlxDjPOwthyDaIQNFcY")


# Connect to SQLite Database
def connect_db():
    return sqlite3.connect("company.db")

# Function to get SQL Query from Hugging Face API
def generate_sql_query(user_input):
    # API_URL = f"https://api-inference.huggingface.co/models/{MODEL_NAME}"
    # headers = {"Authorization": f"Bearer {HUGGINGFACE_API_KEY}"}
    
    database_schema = """
    Our SQLite database has two tables:
    1. Employees (ID, Name, Department, Salary, Hire_Date)
    2. Departments (ID, Name, Manager)
    
    Convert the following natural language question into a valid SQL query using this schema.
    """

    data = {"inputs": f"{database_schema}\nUser Query: {user_input}"}
    model = genai.GenerativeModel("gemini-pro")  
    response = model.generate_content(f"{database_schema}\nUser Query: {user_input}")  # ✅ Correct input


    if not response.text:
        return "Error: No response from AI."
    sql_query = response.text.strip()  

    #  Remove unwanted Markdown formatting (```sql and ```)
    sql_query = re.sub(r"```sql|```", "", sql_query).strip()


    return sql_query


# Process user queries
def process_query(user_input):
    conn = connect_db()
    cursor = conn.cursor()

    ai_query = generate_sql_query(user_input)  # AI generates SQL
    print("Output of AI: ",ai_query)
    try:
        cursor.execute(ai_query)
        results = cursor.fetchall()
        response = results if results else "No data found."
    except Exception as e:
        response = f"Error: {str(e)}"

    conn.close()
    print( response)

# # API Route for the chatbot
# @app.route("/chat", methods=["POST"])
# def chat():
#     data = request.get_json()
#     user_input = data.get("message", "")
#     response = process_query(user_input)
#     return jsonify({"response": response})

# if __name__ == "__main__":
#     app.run(debug=True)

user_input = input("E:")

process_query(user_input)