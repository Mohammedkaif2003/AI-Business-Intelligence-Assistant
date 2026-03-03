import os
import joblib
import re

# Get project root directory
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

model_path = os.path.join(BASE_DIR, "intent_model.pkl")
vectorizer_path = os.path.join(BASE_DIR, "vectorizer.pkl")

model = None
vectorizer = None

try:
    model = joblib.load(model_path)
    vectorizer = joblib.load(vectorizer_path)
except Exception as e:
    print("Model files not found. Using rule-based detection.")

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