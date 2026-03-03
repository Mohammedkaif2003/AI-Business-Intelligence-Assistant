import os
import joblib
import re

# -------------------------
# Load ML Model (Optional)
# -------------------------

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

model_path = os.path.join(BASE_DIR, "intent_model.pkl")
vectorizer_path = os.path.join(BASE_DIR, "vectorizer.pkl")

model = None
vectorizer = None

try:
    model = joblib.load(model_path)
    vectorizer = joblib.load(vectorizer_path)
except Exception:
    print("Model files not found. Using rule-based detection.")


# -------------------------
# Intent Detection
# -------------------------

def detect_intent(query):
    query = query.lower()

    # If ML model exists, use it
    if model and vectorizer:
        vectorized_query = vectorizer.transform([query])
        prediction = model.predict(vectorized_query)
        return prediction[0]

    # Otherwise fallback to rule-based
    if "forecast" in query or "predict" in query:
        return "forecast"

    elif "top" in query or "rank" in query:
        return "ranking"

    elif "growth" in query or "increase" in query:
        return "growth"

    elif "compare" in query:
        return "comparison"

    elif "sales" in query or "revenue" in query:
        return "sales"

    else:
        return "unknown"


# -------------------------
# Entity Extraction
# -------------------------

def extract_entities(query):
    entities = {}

    # Extract year (2020–2039 range)
    year_match = re.search(r'\b(20[2-3][0-9])\b', query)
    if year_match:
        entities["year"] = int(year_match.group())

    # Extract quarter
    quarter_match = re.search(r'\b(Q[1-4])\b', query.upper())
    if quarter_match:
        entities["quarter"] = quarter_match.group()

    # Extract region
    regions = ["north", "south", "east", "west"]
    for region in regions:
        if region in query.lower():
            entities["region"] = region.title()

    # Extract product
    product_match = re.search(r'product\s+\w+', query.lower())
    if product_match:
        entities["product"] = product_match.group().title()

    return entities
