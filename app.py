import streamlit as st
import pandas as pd

# ---------------- IMPORT MODULEFS ----------------
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
from modules.ai_code_generator import generate_analysis_code
from modules.code_executor import execute_code
from modules.question_suggester import suggest_questions
# GROQ AI
from modules.groq_ai import generate_ai_response, suggest_business_questions


# ---------------- API KEY ----------------
api_key = st.secrets["GROQ_API_KEY"]

# TEMP DEBUG
st.write("API Key Loaded:", bool(api_key))


# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="AI Business Intelligence Assistant",
    page_icon="📊",
    layout="wide"
)
st.markdown("""
<style>

/* Page background */
.main {
    background-color: #0e1117;
}

/* Metric cards */
[data-testid="stMetric"] {
    background-color: white;
    padding: 15px;
    border-radius: 12px;
    color: black !important;
}

/* Metric value (numbers) */
[data-testid="stMetricValue"] {
    color: black !important;
    font-size: 28px;
    font-weight: bold;
}

/* Metric label */
[data-testid="stMetricLabel"] {
    color: #555 !important;
}

</style>
""", unsafe_allow_html=True)
st.title("📊 AI Business Intelligence Assistant")

st.markdown(
"""
AI-powered conversational analytics platform for business data.
Upload any dataset and ask questions to generate insights.
"""
)

tab1, tab2, tab3 = st.tabs([
    "📊 Business Dashboard",
    "🤖 AI Data Analyst",
    "📑 Executive Reports"
])


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

product_col = columns.get("Product")
region_col = columns.get("Region")
revenue_col = columns.get("Revenue")
date_col = columns.get("Date")


# ---------------- DATE PROCESSING ----------------
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
    st.divider()
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

    col1.metric(
        label="💰 Total Revenue",
        value=f"${total_revenue:,.0f}",
    )

    col2.metric(
        label="📦 Units Sold",
        value=f"{total_units:,.0f}",
    )

    col3.metric(
        label="🌍 Top Region",
        value=top_region
    )

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
    st.divider()
    st.markdown("### 🤖 Suggested Questions")

    st.info("""
    • Which region generates the highest revenue?
    • Which product has declining sales?
    • What is the monthly revenue trend?
    • Which region contributes most to revenue?
    • Forecast revenue for the next quarter.
    """)

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

                    st.info("AI generating analysis...")

                    # Generate pandas code using AI
                    code = generate_analysis_code(api_key, query, df)

                    result = execute_code(code, df)

                    st.code(code)

                    if isinstance(result, pd.DataFrame):

                        st.dataframe(result)

                        # automatic charts
                        auto_visualize(result)

                        # optional insight generation
                        insight = generate_business_insight(result)
                        st.info(insight)

                    else:

                        st.write(result)

                else:

                    response_text = "Please configure GROQ API key in Streamlit secrets."

        except Exception as e:
            response_text = f"Error: {e}"

        if response_text:

            with st.chat_message("assistant"):
                st.write(response_text)

        if result is not None:

            st.subheader("📊 Analysis Result")

            if isinstance(result, pd.DataFrame):

                st.dataframe(result)

                # automatic charts
                auto_visualize(result)

                # generate business insight
                insight = generate_business_insight(result)

                st.subheader("🧠 Business Insight")
                st.info(insight)

                # AI follow-up suggestions
                if api_key:

                    suggestions = suggest_business_questions(api_key, query, df)

                    st.subheader("💡 Suggested Follow-Up Questions")
                    st.markdown(suggestions)

            else:

                st.write(result)
# =====================================================
# ================= REPORTS ===========================
# =====================================================

with tab3:

    st.subheader("📄 Generate Executive Report")
    st.divider()
    if st.button("Generate PDF Report"):

        file_path = generate_pdf(
            query=query,
            summary_text=insight,
            dataframe=result,
            forecast_value=None
        )

        with open(file_path, "rb") as file:

            st.download_button(
                "Download Report",
                data=file,
                file_name="AI_Executive_Report.pdf",
                mime="application/pdf"
            )