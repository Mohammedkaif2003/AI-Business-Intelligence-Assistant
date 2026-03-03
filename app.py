import streamlit as st

# ---------------- MEMORY ----------------
if "last_entities" not in st.session_state:
    st.session_state["last_entities"] = {}

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# ---------------- STYLING ----------------
st.markdown("""
<style>
.big-title { font-size:28px !important; font-weight:600; }
.metric-card { background-color:#f0f2f6; padding:15px; border-radius:10px; }
.stMetric { background-color:#111827; padding:15px; border-radius:12px; }
</style>
""", unsafe_allow_html=True)

# ---------------- IMPORTS ----------------
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
from modules.insight_engine import generate_executive_insight, generate_executive_paragraph
from modules.auth import login

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="AI Business Intelligence Assistant",
    page_icon="📊",
    layout="wide"
)

login()

st.title("📊 AI Business Intelligence Assistant")
st.markdown("### Conversational Business Analytics System")

tab1, tab2, tab3 = st.tabs(["📊 Dashboard", "💬 AI Chat", "📄 Reports"])

# ---------------- SIDEBAR ----------------
st.sidebar.header("⚙ Dashboard Controls")

years_df = run_query("SELECT DISTINCT Year FROM sales ORDER BY Year")
available_years = years_df["Year"].tolist()

selected_year = st.sidebar.selectbox("Select Year", available_years)

# =====================================================
# ================= DASHBOARD =========================
# =====================================================
with tab1:

    st.markdown("## 📈 Key Business Metrics")

    kpi_query = """
    SELECT SUM(Revenue) as total_revenue,
           SUM(Units_Sold) as total_units
    FROM sales
    WHERE Year = :year
    """
    kpi_data = run_query(kpi_query, {"year": selected_year})

    total_rev = kpi_data["total_revenue"].iloc[0]
    total_units = kpi_data["total_units"].iloc[0]

    growth_query = """
    SELECT 
        SUM(CASE WHEN Year = :current THEN Revenue END) as current_year,
        SUM(CASE WHEN Year = :previous THEN Revenue END) as previous_year
    FROM sales
    WHERE Year IN (:current, :previous)
    """

    growth_data = run_query(
        growth_query,
        {"current": selected_year, "previous": selected_year - 1}
    )

    current_year_val = growth_data["current_year"].iloc[0]
    previous_year_val = growth_data["previous_year"].iloc[0]

    if previous_year_val and previous_year_val != 0:
        growth_percent = ((current_year_val - previous_year_val) / previous_year_val) * 100
    else:
        growth_percent = None

    region_query = """
    SELECT Region, SUM(Revenue) as total_revenue
    FROM sales
    WHERE Year = :year
    GROUP BY Region
    ORDER BY total_revenue DESC
    LIMIT 1
    """
    region_data = run_query(region_query, {"year": selected_year})
    top_region = region_data["Region"].iloc[0] if not region_data.empty else "N/A"

    col1, col2, col3, col4 = st.columns(4)

    col1.metric("Total Revenue", f"{total_rev:,}")
    col2.metric("Units Sold", f"{total_units:,}")
    col3.metric("Top Region", top_region)

    if growth_percent is not None:
        col4.metric("YoY Growth %", f"{round(growth_percent,2)}%",
                    delta=f"{round(growth_percent,2)}%")
    else:
        col4.metric("YoY Growth %", "N/A")

    st.divider()

    paragraph = generate_executive_paragraph(
        total_rev,
        growth_percent,
        top_region
    )

    st.info(paragraph)

# =====================================================
# ================= AI CHAT ===========================
# =====================================================
with tab2:

    st.markdown("## 💬 Ask Business Question")

    query = st.chat_input("Ask your business question...")

    if query:

        with st.chat_message("user"):
            st.write(query)

        intent = detect_intent(query)
        entities = extract_entities(query)

        if entities:
            st.session_state["last_entities"].update(entities)

        year = entities.get("year") or st.session_state["last_entities"].get("year") or selected_year
        region = entities.get("region") or st.session_state["last_entities"].get("region")

        result = None
        response_text = ""

        try:

            if intent == "ranking":
                result = top_products(year)
                response_text = f"Top products in {year}:"

            elif intent == "sales":
                result = total_sales(year)
                total_value = result["Total_Sales"].iloc[0]
                response_text = f"Total sales in {year}: {total_value:,}"

            elif intent == "growth":
                result = revenue_by_region(year, region)
                response_text = f"Revenue breakdown by region in {year}:"

            elif intent == "comparison":
                current = total_sales(year)
                previous = total_sales(year - 1)

                curr_val = current["Total_Sales"].iloc[0]
                prev_val = previous["Total_Sales"].iloc[0]

                growth = ((curr_val - prev_val) / prev_val) * 100

                response_text = (
                    f"{year}: {curr_val:,}\n"
                    f"{year-1}: {prev_val:,}\n\n"
                    f"YoY Growth: {round(growth,2)}%"
                )

            elif intent == "forecast":

                history, forecast, conf_int, risk_level, volatility, trend = forecast_revenue()

                latest_prediction = forecast.iloc[-1]

                response_text = (
                    f"📊 6-Month Forecast\n\n"
                    f"Latest Prediction: {round(latest_prediction,2)}\n"
                    f"Trend: {trend}\n"
                    f"Volatility: {volatility}%\n"
                    f"Risk Level: {risk_level}"
                )

                st.pyplot(plot_forecast(history, forecast, conf_int))

            else:
                response_text = "Sorry, I didn't understand that question."

        except Exception:
            st.error("Unable to process this query.")
            response_text = "Error occurred."

        with st.chat_message("assistant"):
            st.write(response_text)

            if intent == "ranking" and result is not None:
                st.dataframe(result)
                st.pyplot(plot_bar(result, "Product", "Total_Revenue",
                                   f"Top Products in {year}"))
                st.pyplot(plot_pie(result, "Product", "Contribution_%"))
                st.success(generate_executive_insight(result))

            elif intent == "growth" and result is not None:
                st.dataframe(result)
                st.pyplot(plot_bar(result, "Region", "Total_Revenue",
                                   f"Revenue by Region in {year}"))
                st.success(generate_executive_insight(result))

# =====================================================
# ================= REPORTS ===========================
# =====================================================
with tab3:
    st.markdown("## 📄 Executive Reports")

    if st.button("📥 Generate Executive PDF Report"):
        file_path = generate_pdf(
            query="Executive BI Summary",
            summary_text="AI Generated Executive Business Report",
            dataframe=None,
            forecast_value=None
        )

        with open(file_path, "rb") as file:
            st.download_button(
                label="Click to Download",
                data=file,
                file_name="AI_Executive_Report.pdf",
                mime="application/pdf"
            )