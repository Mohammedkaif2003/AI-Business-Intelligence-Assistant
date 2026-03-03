import joblib

model = joblib.load("intent_model.pkl")
vectorizer = joblib.load("vectorizer.pkl")

def detect_intent(query):
    # simple keyword rules take precedence over the ML model
    q_lower = query.lower()
    if any(word in q_lower for word in ["top", "highest", "best", "leading"]):
        return "top_products"
    elif any(word in q_lower for word in ["forecast", "predict", "future"]):
        return "forecast"
    elif any(word in q_lower for word in ["region", "area", "location"]):
        return "region_sales"
    elif any(word in q_lower for word in ["total", "overall", "sum"]):
        return "total_sales"

    # fallback to trained intent classifier
    X = vectorizer.transform([query])
    prediction = model.predict(X)[0]
    return prediction

def extract_year(query):
    for year in ["2024", "2025"]:
        if year in query:
            return int(year)
    return 2025

# keyword-based intent checks are now handled inside detect_intent()