from modules.database import run_query
import pandas as pd
from statsmodels.tsa.arima.model import ARIMA


# -----------------------------
# TOP 5 PRODUCTS
# -----------------------------
def top_products(year):
    if year is None:
        return None

    query = """
    SELECT Product, SUM(Revenue) as Total_Revenue
    FROM sales
    WHERE Year = :year
    GROUP BY Product
    ORDER BY Total_Revenue DESC
    LIMIT 5
    """

    df = run_query(query, {"year": year})

    total_query = """
    SELECT SUM(Revenue) as total
    FROM sales
    WHERE Year = :year
    """

    total_df = run_query(total_query, {"year": year})
    total_revenue = total_df["total"].iloc[0]

    df["Contribution_%"] = round((df["Total_Revenue"] / total_revenue) * 100, 2)

    return df

# -----------------------------
# TOTAL SALES
# -----------------------------
def total_sales(year):
    if year is None:
        return None

    query = f"""
    SELECT SUM(Revenue) as Total_Sales
    FROM sales
    WHERE Year = {year}
    """
    return run_query(query)


# -----------------------------
# REVENUE BY REGION
# -----------------------------
def revenue_by_region(year, region=None):
    if year is None:
        return None

    if region:
        query = """
        SELECT Region, SUM(Revenue) as Total_Revenue
        FROM sales
        WHERE Year = :year AND Region = :region
        GROUP BY Region
        """
        return run_query(query, {"year": year, "region": region})

    else:
        query = """
        SELECT Region, SUM(Revenue) as Total_Revenue
        FROM sales
        WHERE Year = :year
        GROUP BY Region
        """
        return run_query(query, {"year": year})


# -----------------------------
# REVENUE FORECAST (ARIMA)
# -----------------------------
def forecast_revenue():

    query = "SELECT Date, Revenue FROM sales"
    df = run_query(query)

    df["Date"] = pd.to_datetime(df["Date"])

    monthly_data = (
        df.groupby(pd.Grouper(key="Date", freq="M"))["Revenue"]
        .sum()
    )

    model = ARIMA(monthly_data, order=(1, 1, 1))
    model_fit = model.fit()

    forecast = model_fit.forecast(steps=1)

    # Calculate volatility
    volatility = monthly_data.pct_change().std() * 100

    # Risk classification
    if volatility < 5:
        risk_level = "Low"
    elif volatility < 15:
        risk_level = "Medium"
    else:
        risk_level = "High"

    # Trend direction
    if forecast.iloc[0] > monthly_data.iloc[-1]:
        trend = "Upward"
    else:
        trend = "Declining"

    return monthly_data, forecast, risk_level, round(volatility,2), trend
# -----------------------------
# GENERATE SUMMARY (FOR PDF)
# -----------------------------
def generate_summary(query):
    return f"""
    Executive Summary:

    This report analyzes the business query: '{query}'.

    The insights in this report are generated using AI-powered
    data analytics, KPI computation, forecasting models,
    and dynamic visualizations.

    This system acts as a Conversational Business Intelligence Assistant.
    """
def detect_revenue_anomalies():

    query = "SELECT Date, Revenue FROM sales"
    df = run_query(query)

    df["Date"] = pd.to_datetime(df["Date"])

    monthly = df.groupby(pd.Grouper(key="Date", freq="M"))["Revenue"].sum()

    mean = monthly.mean()
    std = monthly.std()

    anomalies = monthly[(monthly > mean + 2*std) | (monthly < mean - 2*std)]

    return monthly, anomalies
