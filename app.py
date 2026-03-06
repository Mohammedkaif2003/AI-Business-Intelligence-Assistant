import streamlit as st
import pandas as pd

# ---------------- IMPORT MODULES ----------------
from modules.analytics_engine import (
    top_products,
    total_sales,
    revenue_by_region,
    forecast_revenue,
    revenue_by_month,
    detect_revenue_anomalies
)

from modules.visualization import plot_forecast
from modules.nlp_processor import detect_intent, extract_entities
from modules.auto_visualizer import auto_visualize
from modules.data_loader import normalize_columns, detect_columns
from modules.insight_engine import generate_business_insight
from modules.report_generator import generate_pdf
from modules.groq_ai import generate_ai_response


# ---------------- API KEY ----------------
api_key = st.secrets["GROQ_API_KEY"]
# TEMP DEBUG LINE
st.write("API Key Loaded:", bool(api_key))

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
st.subheader("📂 Upload Dataset")

uploaded_file = st.file_uploader(
    "Upload your business dataset (CSV)",
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
if "Year" in df.columns:
    available_years = sorted(df["Year"].unique())
    selected_year = st.sidebar.selectbox("Select Year", available_years)
else:
    selected_year = None


# =====================================================
# ================= DASHBOARD =========================
# =====================================================
with tab1:

    st.subheader("📈 Key Business Metrics")

    if selected_year:
        year_df = df[df["Year"] == selected_year]
    else:
        year_df = df

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

    # ---------- Anomaly Detection ----------
    st.subheader("⚠ Revenue Anomaly Detection")

    anomaly_data = detect_revenue_anomalies(df)

    if anomaly_data:

        monthly, anomalies = anomaly_data

        if not anomalies.empty:

            for date, value in anomalies.items():

                st.warning(
                    f"Anomaly detected: {date.strftime('%B %Y')} revenue = {value:,.0f}"
                )

        else:
            st.success("No anomalies detected in revenue trends.")


# =====================================================
# ================= AI CHAT ===========================
# =====================================================
with tab2:

    st.subheader("💬 Ask Business Questions")

    # AI Suggestions
    if api_key:

        st.markdown("### 🤖 AI Suggested Questions")

        suggestions = suggest_business_questions(api_key, df)

        st.info(suggestions)

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

                if api_key:

                    st.info("Using AI to analyze your question...")

                    ai_response = generate_ai_response(api_key, query, df)

                    with st.chat_message("assistant"):
                        st.write(ai_response)

                    response_text = ""

                else:

                    response_text = "Please configure Gemini API key in Streamlit secrets."

        except Exception as e:
            response_text = f"Error: {e}"

        if response_text:

            with st.chat_message("assistant"):
                st.write(response_text)

        if result is not None:

            st.dataframe(result)
            auto_visualize(result)

            insight = generate_business_insight(result)
            st.info(insight)


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