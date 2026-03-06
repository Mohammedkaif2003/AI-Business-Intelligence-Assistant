from google import genai


def generate_ai_response(api_key, query, df):

    client = genai.Client(api_key=api_key)

    dataset_info = f"""
    Dataset columns: {list(df.columns)}
    Sample rows:
    {df.head().to_string()}
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

    response = client.models.generate_content(
        model="gemini-1.5-flash",
        contents=prompt
    )

    return response.text


def suggest_business_questions(api_key, df):

    client = genai.Client(api_key=api_key)

    dataset_info = f"""
    Dataset columns: {list(df.columns)}
    Sample rows:
    {df.head().to_string()}
    """

    prompt = f"""
    Suggest 5 useful business questions that an executive might ask
    based on this dataset.

    Dataset:
    {dataset_info}

    Return short bullet points.
    """

    response = client.models.generate_content(
        model="gemini-2.0-flash",
        contents=prompt
    )

    return response.text