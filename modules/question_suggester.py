from groq import Groq


def suggest_questions(api_key, query, df):

    client = Groq(api_key=api_key)

    prompt = f"""
You are a business analytics assistant.

Dataset columns:
{list(df.columns)}

User asked:
{query}

Suggest 3 follow-up analytical questions the user might ask next.
Return only the questions as bullet points.
"""

    response = client.chat.completions.create(
        model="llama3-70b-8192",
        messages=[{"role": "user", "content": prompt}]
    )

    suggestions = response.choices[0].message.content

    return suggestions