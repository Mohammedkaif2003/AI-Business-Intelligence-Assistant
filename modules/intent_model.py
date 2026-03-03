import pandas as pd
import joblib
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression

def train_intent_model():

    # Training data
    data = {
        "query": [
            "Show top 5 products",
            "Top products by revenue",
            "Which products performed best",
            "Predict next month revenue",
            "Forecast sales",
            "What will revenue be next month",
            "Total sales in 2025",
            "Overall revenue this year",
            "How much did we earn",
            "Revenue by region",
            "Sales region wise",
            "Which region has highest sales"
        ],
        "intent": [
            "top_products",
            "top_products",
            "top_products",
            "forecast",
            "forecast",
            "forecast",
            "total_sales",
            "total_sales",
            "total_sales",
            "region_sales",
            "region_sales",
            "region_sales"
        ]
    }

    df = pd.DataFrame(data)

    vectorizer = TfidfVectorizer()
    X = vectorizer.fit_transform(df["query"])

    model = LogisticRegression()
    model.fit(X, df["intent"])

    joblib.dump(model, "intent_model.pkl")
    joblib.dump(vectorizer, "vectorizer.pkl")

    print("Model trained and saved.")