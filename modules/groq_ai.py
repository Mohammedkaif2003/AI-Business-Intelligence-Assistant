from groq import Groq


def generate_ai_response(api_key, query, df):

    client = Groq(api_key=api_key)

    dataset_info = f"""
    Dataset columns: {list(df.columns)}

    Sample rows:
    {df.head().to_string()}
    """

    prompt = f"""
    You are a business intelligence analyst.

    Dataset:
    {dataset_info}

    User question:
    {query}

    Provide:
    - Analysis
    - Business insight
    - Recommendation
    """

    response = client.chat.completions.create(
        model="llama3-70b-8192",
        messages=[
            {"role": "user", "content": prompt}
        ]
    )

    return response.choices[0].message.content


def suggest_business_questions(api_key, df):

    client = Groq(api_key=api_key)

    dataset_info = f"""
    Dataset columns: {list(df.columns)}

    Sample rows:
    {df.head().to_string()}
    """

    prompt = f"""
    Suggest 5 useful business questions that an executive
    might ask about this dataset.
    """

    response = client.chat.completions.create(
        model="llama3-70b-8192",
        messages=[
            {"role": "user", "content": prompt}
        ]
    )

    return response.choices[0].message.content