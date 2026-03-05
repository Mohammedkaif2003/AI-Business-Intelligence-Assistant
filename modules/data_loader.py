import pandas as pd


def normalize_columns(df):

    df.columns = df.columns.str.strip()

    mapping = {
        "sales": "Revenue",
        "sales_amount": "Revenue",
        "revenue_amount": "Revenue",
        "product_name": "Product",
        "item": "Product",
        "item_name": "Product",
        "location": "Region",
        "area": "Region",
        "order_date": "Date"
    }

    df.rename(columns=mapping, inplace=True)

    return df


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