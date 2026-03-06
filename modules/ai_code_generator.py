from groq import Groq


def generate_analysis_code(api_key, query, df):

    client = Groq(api_key=api_key)

    prompt = f"""
You are a Python data analyst.

The dataframe is called df.

Columns:
{list(df.columns)}

User question:
{query}

Write ONLY Python pandas code to answer the question.

Rules:
- Use dataframe name df
- Return the result in variable called result
- Do not include explanations
"""

    response = client.chat.completions.create(
        model="llama3-70b-8192",
        messages=[{"role": "user", "content": prompt}],
    )

    code = response.choices[0].message.content

    return code