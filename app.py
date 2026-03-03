import streamlit as st
if "last_entities" not in st.session_state:
    st.session_state["last_entities"] = {}
st.markdown("""
<style>
.big-title {
    font-size:28px !important;
    font-weight:600;
}
.metric-card {
    background-color:#f0f2f6;
    padding:15px;
    border-radius:10px;
}
</style>
""", unsafe_allow_html=True)
from modules.analytics_engine import (
    top_products,
    total_sales,
    revenue_by_region,
    forecast_revenue,
    generate_summary
)
from modules.visualization import plot_bar, plot_forecast, plot_pie
from modules.nlp_processor import detect_intent, extract_entities
from modules.report_generator import generate_pdf
from modules.database import run_query
from modules.insight_engine import generate_executive_insight
from modules.auth import login

# ------------------ PAGE CONFIG ------------------
st.set_page_config(
    page_title="AI Business Intelligence Assistant",
    page_icon="📊",
    layout="wide"
)
login()
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

st.title("📊 AI Business Intelligence Assistant")
tab1, tab2, tab3 = st.tabs(["📊 Dashboard", "💬 AI Chat", "📄 Reports"])
st.markdown("### Conversational Business Analytics System")

# ------------------ SIDEBAR ------------------
st.sidebar.header("⚙ Dashboard Controls")

# Get available years from DB
years_df = run_query("SELECT DISTINCT Year FROM sales ORDER BY Year")
available_years = years_df["Year"].tolist()

selected_year = st.sidebar.selectbox(
    "Select Year",
    available_years
)

# ------------------ KPI SECTION ------------------
with tab1:
    st.markdown("## 📈 Key Business Metrics")

    kpi_query = f"""
    SELECT 
        SUM(Revenue) as total_revenue,
     SUM(Units_Sold) as total_units
    FROM sales
    WHERE Year = {selected_year}
    """
    kpi_data = run_query(kpi_query)

    total_rev = kpi_data["total_revenue"].iloc[0]
    # -------- YoY Growth Calculation --------
    growth_query = f"""
    SELECT 
        SUM(CASE WHEN Year = {selected_year} THEN Revenue END) as current_year,
        SUM(CASE WHEN Year = {selected_year - 1} THEN Revenue END) as previous_year
    FROM sales
    WHERE Year IN ({selected_year}, {selected_year - 1})
    """

    growth_data = run_query(growth_query)

    current_year = growth_data["current_year"].iloc[0]
    previous_year = growth_data["previous_year"].iloc[0]

    if previous_year is not None and previous_year != 0:
        growth_percent = ((current_year - previous_year) / previous_year) * 100
    else:
        growth_percent = None
    total_units = kpi_data["total_units"].iloc[0]

    region_query = f"""
    SELECT Region, SUM(Revenue) as total_revenue
    FROM sales
    WHERE Year = {selected_year}
    GROUP BY Region
    ORDER BY total_revenue DESC
    LIMIT 1
    """
    region_data = run_query(region_query)
    if not region_data.empty:
        top_region = region_data["Region"].iloc[0]
    else:
        top_region = "N/A"
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Total Revenue", f"{total_rev:,}")
    col2.metric("Units Sold", f"{total_units:,}")
    col3.metric("Top Performing Region", top_region)
    if growth_percent is not None:
        col4.metric(
            "YoY Growth %",
            f"{round(growth_percent,2)}%",
            delta=f"{round(growth_percent,2)}%"
        )
    else:
        col4.metric("YoY Growth %", "N/A")
    st.divider()
    from modules.insight_engine import generate_executive_paragraph

    paragraph = generate_executive_paragraph(
        total_rev,
        growth_percent,
        top_region
)

st.info(paragraph)

# ------------------ CHAT SECTION ------------------
with tab2:
    st.markdown("## 💬 Ask Business Question")

query = st.chat_input("Ask your business question...")

if query:

    with st.chat_message("user"):
        st.write(query)

    intent = detect_intent(query)
    entities = extract_entities(query)

    # Save memory
    if entities:
        st.session_state["last_entities"].update(entities)

    # Use memory fallback
    year = entities.get("year") or st.session_state["last_entities"].get("year") or selected_year
    region = entities.get("region") or st.session_state["last_entities"].get("region")

    year = entities.get("year", selected_year)
    region = entities.get("region")

    result = None
    predicted_value = None
    response_text = ""

    try:
        # -------- INTENT LOGIC --------
        if intent == "ranking":
            result = top_products(year)
            response_text = f"Here are the top products for {year}."

        elif intent == "sales":
            result = total_sales(year)
            total_value = result["Total_Sales"].iloc[0]
            response_text = f"Total sales in {year} is {total_value:,}."

        elif intent == "growth":
            result = revenue_by_region(year, region)
            response_text = f"Here is revenue breakdown by region for {year}."

        elif intent == "forecast":
            history, forecast, risk_level, volatility, trend = forecast_revenue()
            predicted_value = forecast.iloc[0]

            response_text = (
                f"Predicted revenue for next month is {round(predicted_value,2)}.\n\n"
                f"Trend: {trend}\n"
                f"Volatility: {volatility}%\n"
                f"Forecast Risk Level: {risk_level}"
            )

        else:
            response_text = "Sorry, I didn't understand that question."

    except Exception:
        st.error("Unable to process this query.")
        response_text = "Error occurred while processing."

    with st.chat_message("assistant"):
        st.write(response_text)

        # -------- VISUALIZATION --------
        if intent == "ranking" and result is not None:
            st.dataframe(result)

            fig = plot_bar(result, "Product", "Total_Revenue",
                           f"Top Products in {year}")
            st.pyplot(fig)

            pie_fig = plot_pie(result, "Product", "Contribution_%",
                               "Revenue Contribution Share")
            st.pyplot(pie_fig)

            insight_text = generate_executive_insight(result)
            st.success(insight_text)

        elif intent == "growth" and result is not None:
            st.dataframe(result)

            fig = plot_bar(result, "Region", "Total_Revenue",
                           f"Revenue by Region in {year}")
            st.pyplot(fig)

            insight_text = generate_executive_insight(result)
            st.success(insight_text)

        elif intent == "forecast" and predicted_value is not None:
            fig = plot_forecast(history, forecast)
            st.pyplot(fig)

            from modules.analytics_engine import detect_revenue_anomalies
            monthly_data, anomalies = detect_revenue_anomalies()

            if not anomalies.empty:
                st.warning("⚠ Revenue anomaly detected in:")
                st.write(anomalies)

    summary = generate_summary(query)

    with tab3:
        st.markdown("## 📄 Executive Reports")
        if st.button("📥 Generate Executive PDF Report"):

            file_path = generate_pdf(
                query=query,
                summary_text=summary,
                dataframe=result,
                forecast_value=predicted_value
            )

            with open(file_path, "rb") as file:
                st.download_button(
                    label="Click to Download",
                    data=file,
                    file_name="AI_Executive_Report.pdf",
                    mime="application/pdf"
                )