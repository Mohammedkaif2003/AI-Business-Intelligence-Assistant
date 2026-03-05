import streamlit as st
import pandas as pd

# ---------------- IMPORT MODULES ----------------
from modules.analytics_engine import (
    top_products,
    total_sales,
    revenue_by_region,
    forecast_revenue,
    revenue_by_month
)

from modules.visualization import plot_forecast
from modules.nlp_processor import detect_intent, extract_entities
from modules.auto_visualizer import auto_visualize
from modules.data_loader import normalize_columns, detect_columns
from modules.report_generator import generate_pdf


# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="AI Business Intelligence Assistant",
    page_icon="📊",
    layout="wide"
)

st.title("📊 AI Business Intelligence Assistant")
st.markdown("### Conversational Business Analytics System")

tab1, tab2, tab3 = st.tabs(["📊 Dashboard", "💬 AI Chat", "📄 Reports"])


# ---------------- FILE UPLOAD ----------------
st.sidebar.header("📂 Upload Dataset")

uploaded_file = st.sidebar.file_uploader(
    "Upload CSV dataset",
    type=["csv"]
)

if uploaded_file is None:
    st.warning("Please upload a dataset to start.")
    st.stop()

df = pd.read_csv(uploaded_file)

df = normalize_columns(df)
columns = detect_columns(df)

# Extract important columns
product_col = columns.get("Product")
region_col = columns.get("Region")
revenue_col = columns.get("Revenue")
date_col = columns.get("Date")

# Convert date column
if date_col:
    df[date_col] = pd.to_datetime(df[date_col])
    df["Year"] = df[date_col].dt.year
    df["Month"] = df[date_col].dt.month


# ---------------- YEAR SELECTION ----------------
available_years = sorted(df["Year"].unique())
selected_year = st.sidebar.selectbox("Select Year", available_years)


# =====================================================
# ================= DASHBOARD =========================
# =====================================================
with tab1:

    st.subheader("📈 Key Business Metrics")

    year_df = df[df["Year"] == selected_year]

    total_revenue = year_df[revenue_col].sum()

    total_units = 0
    if "Units_Sold" in df.columns:
        total_units = year_df["Units_Sold"].sum()

    region_data = (
        year_df.groupby(region_col)[revenue_col]
        .sum()
        .reset_index()
        .sort_values(by=revenue_col, ascending=False)
    )

    top_region = region_data.iloc[0][region_col]

    col1, col2, col3 = st.columns(3)

    col1.metric("Total Revenue", f"{total_revenue:,.0f}")
    col2.metric("Units Sold", f"{total_units:,.0f}")
    col3.metric("Top Region", top_region)

    st.dataframe(region_data)
    auto_visualize(region_data)


# =====================================================
# ================= AI CHAT ===========================
# =====================================================
with tab2:

    st.subheader("💬 Ask Business Questions")

    query = st.chat_input("Ask something about your business data...")

    if query:

        with st.chat_message("user"):
            st.write(query)

        intent = detect_intent(query)
        entities = extract_entities(query)

        year = entities.get("year", selected_year)
        region = entities.get("region")

        result = None
        response_text = ""

        try:

            if intent == "ranking":

                result = top_products(df, year)
                response_text = f"Top products in {year}"

            elif intent == "sales":

                result = total_sales(df, year)
                total_value = result["Total_Sales"].iloc[0]
                response_text = f"Total sales in {year}: {total_value:,.0f}"

            elif intent == "growth":

                result = revenue_by_region(df, year, region)
                response_text = f"Revenue by region in {year}"

            elif intent == "monthly_sales":

                result = revenue_by_month(df, year)
                response_text = f"Monthly revenue in {year}"

            elif intent == "forecast":

                forecast_data = forecast_revenue(df)

                if forecast_data is None:
                    response_text = "Not enough data to generate forecast."

                else:

                    history, forecast = forecast_data

                    response_text = "Revenue forecast generated."

                    fig = plot_forecast(history, forecast)
                    st.pyplot(fig)

            else:
                response_text = "Sorry, I couldn't understand that question."

        except Exception as e:
            response_text = f"Error: {e}"

        with st.chat_message("assistant"):
            st.write(response_text)

        if result is not None:
            st.dataframe(result)
            auto_visualize(result)


# =====================================================
# ================= REPORTS ===========================
# =====================================================
with tab3:

    st.subheader("📄 Generate Executive Report")

    if st.button("Generate PDF Report"):

        file_path = generate_pdf(
            query="Business Analytics Summary",
            summary_text="AI Generated Business Intelligence Report",
            dataframe=None,
            forecast_value=None
        )

        with open(file_path, "rb") as file:
            st.download_button(
                "Download Report",
                data=file,
                file_name="BI_Report.pdf",
                mime="application/pdf"
            )