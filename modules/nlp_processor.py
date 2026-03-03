import joblib

model = joblib.load("intent_model.pkl")
vectorizer = joblib.load("vectorizer.pkl")

def detect_intent(query):
    query = query.lower()

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

# keyword-based intent checks are now handled inside detect_intent()
import re

def extract_entities(query):
    entities = {}

    # Extract year (2020–2030 range)
    year_match = re.search(r'\b(20[2-3][0-9])\b', query)
    if year_match:
        entities["year"] = int(year_match.group())

    # Extract quarter
    quarter_match = re.search(r'\b(Q[1-4])\b', query.upper())
    if quarter_match:
        entities["quarter"] = quarter_match.group()

    # Extract region (customize based on dataset)
    regions = ["north", "south", "east", "west"]
    for region in regions:
        if region in query.lower():
            entities["region"] = region.title()

    # Extract product (if dataset has product column)
    # Example: "Product A", "Product X"
    product_match = re.search(r'product\s+\w+', query.lower())
    if product_match:
        entities["product"] = product_match.group().title()

    return entities