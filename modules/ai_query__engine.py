import ollama
import pandas as pd

def run_ai_query(df, query):

    prompt = f"""
    You are a Python data analyst.

    Dataset columns:
    {list(df.columns)}

    User question:
    {query}

    Write Python pandas code to answer the question.
    Use matplotlib if chart is required.
    Only output python code.
    """

    response = ollama.chat(
        model="llama3",
        messages=[{"role": "user", "content": prompt}]
    )

    code = response["message"]["content"]

    return code

def execute_ai_code(code, df):

    local_vars = {"df": df}

    exec(code, {}, local_vars)

    return local_vars
if "import os" in code or "import sys" in code:
    raise ValueError("Unsafe code generated")