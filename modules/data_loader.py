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