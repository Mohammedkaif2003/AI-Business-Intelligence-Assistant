import pandas as pd
from statsmodels.tsa.arima.model import ARIMA


# -----------------------------
# TOP 5 PRODUCTS
# -----------------------------
def top_products(df, year):

    df_year = df[df["Year"] == year]

    result = (
        df_year.groupby("Product")["Revenue"]
        .sum()
        .reset_index()
        .sort_values(by="Revenue", ascending=False)
        .head(5)
    )

    total_revenue = result["Revenue"].sum()

    if total_revenue > 0:
        result["Contribution_%"] = round(
            (result["Revenue"] / total_revenue) * 100, 2
        )
    else:
        result["Contribution_%"] = 0

    return result


# -----------------------------
# TOTAL SALES
# -----------------------------
def total_sales(df, year):

    df_year = df[df["Year"] == year]

    total = df_year["Revenue"].sum()

    return pd.DataFrame({"Total_Sales": [total]})


# -----------------------------
# REVENUE BY REGION
# -----------------------------
def revenue_by_region(df, year, region=None):

    df_year = df[df["Year"] == year]

    if region:
        df_year = df_year[df_year["Region"] == region]

    result = (
        df_year.groupby("Region")["Revenue"]
        .sum()
        .reset_index()
        .sort_values(by="Revenue", ascending=False)
    )

    return result


# -----------------------------
# REVENUE BY MONTH
# -----------------------------
def revenue_by_month(df, year):

    df_year = df[df["Year"] == year]

    result = (
        df_year.groupby("Month")["Revenue"]
        .sum()
        .reset_index()
        .sort_values(by="Month")
    )

    return result


# -----------------------------
# FORECAST REVENUE (ARIMA)
# -----------------------------
def forecast_revenue(df, steps=6):

    df["Date"] = pd.to_datetime(df["Date"])

    monthly_data = (
        df.groupby(pd.Grouper(key="Date", freq="M"))["Revenue"]
        .sum()
    )

    if len(monthly_data) < 6:
        return None

    model = ARIMA(monthly_data, order=(1,1,1))
    model_fit = model.fit()

    forecast = model_fit.forecast(steps=steps)

    return monthly_data, forecast


# -----------------------------
# SUMMARY FOR REPORT
# -----------------------------
def generate_summary(query):

    return f"""
Executive Summary:

This report analyzes the business query: '{query}'.

The insights in this report are generated using AI-powered
data analytics and dynamic visualizations.
"""


# -----------------------------
# ANOMALY DETECTION
# -----------------------------
def detect_revenue_anomalies(df):

    df["Date"] = pd.to_datetime(df["Date"])

    monthly = df.groupby(pd.Grouper(key="Date", freq="M"))["Revenue"].sum()

    mean = monthly.mean()
    std = monthly.std()

    anomalies = monthly[
        (monthly > mean + 2*std) |
        (monthly < mean - 2*std)
    ]

    return monthly, anomalies