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
def run_query(query, params=None):
    df = load_data()

    # filter by year if provided
    if params and "year" in params:
        df = df[df["Year"] == params["year"]]

    # KPI query
    if "total_revenue" in query.lower():
        total_revenue = df["Revenue"].sum()
        return pd.DataFrame({"total_revenue": [total_revenue]})

    return df