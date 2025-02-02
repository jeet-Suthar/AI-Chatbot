import os
os.environ["GRPC_ENABLE_FORK_SUPPORT"] = "0"  # Fix gRPC shutdown warnings
os.environ["TF_CPP_MIN_LOG_LEVEL"] = "2"  # Suppress TensorFlow logs
import re
import sqlite3
import requests
from flask import Flask, request, render_template, jsonify
from flask_cors import CORS 
import google.generativeai as genai

app = Flask(__name__)
CORS(app) # cross origin resource sharing function


# Set up Gemini API Key
genai.configure(api_key="AIzaSyCC6iznCyPjfZjRHlxDjPOwthyDaIQNFcY")


# Connect to SQLite Database
def connect_db():
    return sqlite3.connect("company.db")

# Function to get SQL Query from Hugging Face API
def generate_ai_response(user_input,model_name):
    # API_URL = f"https://api-inference.huggingface.co/models/{MODEL_NAME}"
    # headers = {"Authorization": f"Bearer {HUGGINGFACE_API_KEY}"}
    
    database_schema = """
   You are an SQL expert. Convert natural language queries into valid SQLite queries based on the following schema:  

    Departments Table
    - Dept_ID (INTEGER, PRIMARY KEY)  
    - Dept_Name (TEXT, UNIQUE, NOT NULL)  
    - Manager_ID (INTEGER)  
    - Budget (REAL)  
    - Location (TEXT)  
    - Established_Date (DATE)  

    Employees Table
    - Emp_ID (INTEGER, PRIMARY KEY)  
    - First_Name (TEXT, NOT NULL)  
    - Last_Name (TEXT, NOT NULL)  
    - Dept_ID (INTEGER, FOREIGN KEY → Departments.Dept_ID)  
    - Position (TEXT)  
    - Salary (REAL)  
    - Hire_Date (DATE)  
    - Email (TEXT, UNIQUE)  
    - Phone (TEXT)  

    Rules
    - Only generate `SELECT` queries. Do not generate `DELETE`, `UPDATE`, `DROP`, or `ALTER` queries.  
    - Query which are not related to sql should be answered in text format precedding with *
    """

    data = {"inputs": f"{database_schema}\n User Query: {user_input}"}
    print("user input is : ",user_input)
    
    
    # model selection will be performed here...let
    print("\n\nDATA GIVEN TO AI :", data, "\n\nData type : ", type(data))
    
    if(model_name == "Gemini"):
        
        print("\n\n ab GEMINI answer deg\n\na")
    
        model = genai.GenerativeModel("gemini-pro")  
        response = model.generate_content(f"{database_schema}\nUser Query: {user_input}")  # ✅ Correct input

    else:
        
        print("\n\n ab OpenAI ka rival...DeepSeek answer dega\n\n")
        
        HF_API_URL = "https://jeetsuthar-test5.hf.space/chat" # link to my hugging face docker API where i uploaded deepseek model and build FastAPI application
        headers = {"Content-Type": "application/json"}
        msg = {"message": f"{database_schema}\nUser Query: {user_input}"}
        response = requests.post(HF_API_URL, json=msg, headers=headers)
        
        print("\n\n --------------Resonse from deepseek-----------\n\n", response.text) # dedugging ke hetu istmal kiya gya 

        if response.ok: 
            
            return response.json()  # Return response data
        else:
            return {"error": "Failed to get response from Hugging Face API"}



    if not response.text:
        return "Error: No response from AI."
    ai_response = response.text.strip()  

    #  Remove unwanted Markdown formatting (```sql and ```)
    
    ai_response = re.sub(r"```sql|```", "", ai_response).strip()


    return ai_response





# Process user queries
def process_query(user_input,model_name):
    conn = connect_db()
    cursor = conn.cursor()

    ai_query = generate_ai_response(user_input,model_name)  # AI generates SQL
    print("Output of AI: ",ai_query)
    
    # check if model is deepseek then it will just return response  
    if(model_name == "DeepSeek"):
        return {"type": "text", "data": ai_query["response"]}
        
    # ye RegeX ka use karke dept name extract karega query se    
    dept_name = extract_department_name(ai_query)
    
    # ye normal text response ke hetu hai !!
    if ai_query.startswith("*"):
        response = {"type": "text", "data": ai_query.lstrip("*").strip()}  # Remove * and extra spaces
        
    # nimanlikhit 2 lines department ke valid naam check karne hetu hai !!!
    elif dept_name and not is_valid_department(dept_name):
        response =  {"type": "text", "data": "Invalid department name. No matching data found."}
        
    else:
        try:
            cursor.execute(ai_query)
            results = cursor.fetchall()
            if results:
                response = {
                    "type": "table",  # is se table banega frontend pe
                    "data": [dict(zip([column[0] for column in cursor.description], row)) for row in results] # process dict
                }
            else:
                response = {"type": "text", "data": "No data found."}
        except Exception as e:
            print("yaha bhi chud gye guru")
            response =  {"type": "text", "data": "Oops! We f*cked up...try again later. :)"}
            # response = {"type": "text", "data": f"Error: {str(e)}"}

    print("Final Response:", response)

    conn.close()
    return response

# API Route for the chatbot

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json()
    print("This is whole json receeived : ", data)
    user_input = data.get("message", "") # isme user prompt hai
    model_name = data.get("model","") # isme model ka naam hai 
    
    
    print("THIS IS RAW MSG : ",user_input)
    
    # ab sabse mushkil part...choosing gemini and deepseek model when user says
    # aur uska sahi se answer dena
    
    
    response = process_query(user_input,model_name)
    return jsonify({"response": response})
    # user_input = input("E:")

    # process_query(user_input)
    
def is_valid_department(dept_name):
    """Checks if the department exists in the database."""
    conn = connect_db()
    cursor = conn.cursor()
    print("dpt name striped ", dept_name)
    cursor.execute("SELECT COUNT(*) FROM Departments WHERE Dept_Name = ?", (dept_name,))
    result = cursor.fetchone()[0]  # count milega isse
    
    conn.close()
    print("department name here :", result)
    return result > 0  


# this will use regex expresssion to get out department name
def extract_department_name(ai_query):
    """Extracts department name from an AI-generated SQL query safely."""
    match = re.search(r"Dept_Name\s*=\s*'([^']+)'", ai_query, re.IGNORECASE)
    return match.group(1) if match else None  # Returns department name or None

if __name__ == "__main__":
    app.run(debug=True)

# if __name__ == "__main__":
#     app.run(host="0.0.0.0", port=10000)  # Change port 
