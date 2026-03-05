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

    df["Contribution_%"] = round(
        (df["Total_Revenue"] / total_revenue) * 100, 2)

    return df

# -----------------------------
# TOTAL SALES
# -----------------------------


def total_sales(year):
    if year is None:
        return None

    query = """
    SELECT SUM(Revenue) as Total_Sales
    FROM sales
    WHERE Year = :year
    """
    return run_query(query, {"year": year})


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


"""AND LOWER(Region) = LOWER(:region)"""


def revenue_by_month(year):

    query = """
    SELECT 
        strftime('%m', Date) as Month,
        SUM(Revenue) as Total_Revenue
    FROM sales
    WHERE Year = :year
    GROUP BY Month
    ORDER BY Month
    """

    df = run_query(query, {"year": year})

    # Convert Month from string to integer
    df["Month"] = df["Month"].astype(int)

    return df


# -----------------------------
# REVENUE FORECAST (ARIMA)
# -----------------------------
if len(monthly_data) < 6:
    return None


def forecast_revenue(steps=6):

    query = "SELECT Date, Revenue FROM sales"
    df = run_query(query)

    df["Date"] = pd.to_datetime(df["Date"])

    monthly_data = (
        df.groupby(pd.Grouper(key="Date", freq="M"))["Revenue"]
        .sum()
    )

    model = ARIMA(monthly_data, order=(1, 1, 1))
    model_fit = model.fit()

    forecast_object = model_fit.get_forecast(steps=steps)

    forecast_values = forecast_object.predicted_mean
    conf_int = forecast_object.conf_int()

    # Create proper forecast index
    forecast_values.index = pd.date_range(
        start=monthly_data.index[-1] + pd.DateOffset(months=1),
        periods=steps,
        freq="M"
    )

    conf_int.index = forecast_values.index

    volatility = monthly_data.pct_change().std() * 100

    if volatility < 5:
        risk_level = "Low"
    elif volatility < 15:
        risk_level = "Medium"
    else:
        risk_level = "High"

    if forecast_values.iloc[-1] > monthly_data.iloc[-1]:
        trend = "Upward"
    else:
        trend = "Declining"

    return monthly_data, forecast_values, conf_int, risk_level, round(volatility, 2), trend
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
