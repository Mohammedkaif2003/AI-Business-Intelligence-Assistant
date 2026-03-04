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

    if "forecast" in query or "predict" in query:
        return "forecast"

    elif any(word in query for word in ["top","rank","best","highest","most"]):
        return "ranking"

    elif "compare" in query or "previous year" in query or "last year" in query:
        return "comparison"

    elif "month" in query or "trend" in query:
        return "monthly_sales"

    elif "region" in query:
        return "growth"

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
