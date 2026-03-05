import pandas as pd

def load_data():
    df = pd.read_csv("data/company_data.csv")
    df["Date"] = pd.to_datetime(df["Date"])
    df["Year"] = df["Date"].dt.year
    df["Month"] = df["Date"].dt.month
    df["Quarter"] = df["Date"].dt.quarter
    return df
def normalize_columns(df):

    mapping = {
        "sales": "Revenue",
        "sales_amount": "Revenue",
        "product_name": "Product",
        "item": "Product",
        "location": "Region",
        "area": "Region"
    }

    df.rename(columns=mapping, inplace=True)

    return df
def detect_value_column(df):

    numeric_cols = df.select_dtypes(include="number").columns

    if len(numeric_cols) > 0:
        return numeric_cols[0]

    return None
def detect_columns(df):

    column_map = {}

    for col in df.columns:

        name = col.lower()

        if "product" in name or "item" in name:
            column_map["Product"] = col

        elif "region" in name or "location" in name or "area" in name:
            column_map["Region"] = col

        elif "revenue" in name or "sales" in name:
            column_map["Revenue"] = col

        elif "date" in name:
            column_map["Date"] = col

    return column_map
def run_query(query):
    df = load_data()

    # support: SELECT DISTINCT Year FROM sales ORDER BY Year
    if "SELECT DISTINCT Year" in query:
        years = sorted(df["Year"].unique())
        return pd.DataFrame({"Year": years})

    return df