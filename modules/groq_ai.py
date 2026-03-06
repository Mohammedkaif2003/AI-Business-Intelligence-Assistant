from groq import Groq


def generate_ai_response(api_key, query, df):

    client = Groq(api_key=api_key)

    dataset_info = f"""
    Dataset Columns: {list(df.columns)}
    Total Rows: {len(df)}
    """

    prompt = f"""
    You are a business intelligence analyst.

    Dataset information:
    {dataset_info}

    User question:
    {query}

    Provide:
    - Analysis
    - Business insight
    - Recommendation
    """

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {"role": "user", "content": prompt}
        ],
        temperature=0.3
    )

    return response.choices[0].message.content



def suggest_business_questions(api_key, df):

    client = Groq(api_key=api_key)

    dataset_info = f"""
    Dataset Columns: {list(df.columns)}
    Total Rows: {len(df)}
    """

    prompt = f"""
    Suggest 5 useful business questions
    that an executive might ask about this dataset.
    """

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {"role": "user", "content": prompt}
        ],
        temperature=0.3
    )

    return response.choices[0].message.content