import google.generativeai as genai


def generate_ai_response(api_key, query, df):

    genai.configure(api_key=api_key)

    model = genai.GenerativeModel("gemini-1.5-flash")

    # Give AI dataset context
    dataset_info = f"""
    Dataset Columns: {list(df.columns)}
    Number of rows: {len(df)}

    First 5 rows:
    {df.head().to_string()}
    """

    prompt = f"""
    You are a business intelligence analyst.

    Dataset info:
    {dataset_info}

    User question:
    {query}

    Answer with:
    1. Analysis
    2. Business insight
    3. Recommendation
    """

    response = model.generate_content(prompt)

    return response.text

def suggest_business_questions(api_key, df):

    genai.configure(api_key=api_key)

    model = genai.GenerativeModel("gemini-1.5-flash")

    dataset_info = f"""
    Dataset columns: {list(df.columns)}
    Sample rows:
    {df.head().to_string()}
    """

    prompt = f"""
    You are a business intelligence expert.

    Based on this dataset, suggest 5 useful business questions
    an executive might ask.

    Dataset:
    {dataset_info}

    Return short questions only.
    """

    response = model.generate_content(prompt)

    return response.text