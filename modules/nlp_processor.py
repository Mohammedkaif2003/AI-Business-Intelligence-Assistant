import re


# -------------------------
# INTENT DETECTION
# -------------------------
def detect_intent(query):

    query = query.lower()

    if "forecast" in query or "predict" in query:
        return "forecast"

    elif any(word in query for word in ["top", "rank", "best", "highest", "most"]):
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
# ENTITY EXTRACTION
# -------------------------
def extract_entities(query):

    entities = {}

    query_lower = query.lower()

    # Extract year
    year_match = re.search(r"\b(20[2-3][0-9])\b", query_lower)
    if year_match:
        entities["year"] = int(year_match.group())

    # Extract quarter
    quarter_match = re.search(r"\b(q[1-4])\b", query_lower)
    if quarter_match:
        entities["quarter"] = quarter_match.group().upper()

    # Extract region
    regions = ["north", "south", "east", "west"]

    for region in regions:
        if region in query_lower:
            entities["region"] = region.title()

    # Extract product
    product_match = re.search(r"product\s+([\w\s]+)", query_lower)
    if product_match:
        entities["product"] = product_match.group(1).title()

    return entities


# -------------------------
# OPTIONAL HELPERS
# -------------------------
def extract_product(query, df):

    if "Product" not in df.columns:
        return None

    for product in df["Product"].unique():

        if product.lower() in query.lower():
            return product

    return None