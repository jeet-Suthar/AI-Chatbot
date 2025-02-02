from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from transformers import AutoModelForCausalLM, AutoTokenizer
import sqlite3
import torch

app = FastAPI()

# Load the DeepSeek model and tokenizer
MODEL_NAME = "deepseek-ai/deepseek-coder-1.3b-instruct"
tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
model = AutoModelForCausalLM.from_pretrained(MODEL_NAME, torch_dtype=torch.float32).to("cpu")


class ChatRequest(BaseModel):
    message: str

def generate_sql_query(user_input: str) -> str:
    """
    Generate an SQL query from a natural language query using the DeepSeek model.
    """
    inputs = tokenizer(user_input, return_tensors="pt", padding="longest", truncation=True)
    outputs = model.generate(**inputs, max_length=400, do_sample=False, num_beams=1)
    sql_query = tokenizer.decode(outputs[0], skip_special_tokens=True)

    return sql_query


@app.post("/chat")
def chat(request: ChatRequest):
    user_input = request.message
    
    sql_query = generate_sql_query(user_input)
    print(f"Generated SQL Query: {sql_query}")

    return {"response": sql_query}

@app.get("/")
def home():
    return {"message": "DeepSeek SQL Query API is running"}