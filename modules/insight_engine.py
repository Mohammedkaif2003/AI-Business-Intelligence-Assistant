import pandas as pd

def generate_executive_insight(df):

    if df is None or df.empty:
        return "No data available for insight generation."

    insights = []

    # ---------------------------
    # Revenue Analysis
    # ---------------------------
    if "Total_Revenue" in df.columns:

        total = df["Total_Revenue"].sum()
        max_value = df["Total_Revenue"].max()
        min_value = df["Total_Revenue"].min()

        max_share = (max_value / total) * 100
        min_share = (min_value / total) * 100

        # Concentration Risk
        if max_share > 50:
            insights.append(
                f"⚠ High revenue concentration: Top entity contributes {round(max_share,2)}%."
            )

        elif max_share > 35:
            insights.append(
                f"⚠ Moderate dependency: Top entity contributes {round(max_share,2)}%."
            )

        # Weak Performer
        if min_share < 8:
            insights.append(
                f"📉 Weak performance detected: Lowest contributor accounts for only {round(min_share,2)}%."
            )

        # Revenue Spread Check
        spread_ratio = max_value / min_value if min_value != 0 else 0

        if spread_ratio > 4:
            insights.append(
                "⚖ Large performance gap between top and bottom performers."
            )

    # ---------------------------
    # Region Analysis
    # ---------------------------
    if "Region" in df.columns and "Total_Revenue" in df.columns:
        top_region = df.sort_values("Total_Revenue", ascending=False).iloc[0]["Region"]
        insights.append(f"🏆 {top_region} region leads overall revenue contribution.")

    # ---------------------------
    # Contribution % Based Check
    # ---------------------------
    if "Contribution_%" in df.columns:
        top_share = df["Contribution_%"].iloc[0]

        if top_share > 45:
            insights.append(
                f"⚠ Strategic risk: Heavy reliance on a single product ({top_share}%)."
            )

    # ---------------------------
    # Final Output
    # ---------------------------
    if not insights:
        return "✅ Revenue distribution appears stable with no major risk indicators."

    return " ".join(insights)
def generate_executive_paragraph(total_rev, growth_percent, top_region):

    paragraph = f"In the selected year, total revenue reached {total_rev:,.0f}."

    if growth_percent is not None:
        if growth_percent > 0:
            paragraph += f" This represents a positive year-over-year growth of {round(growth_percent,2)}%."
        else:
            paragraph += f" This reflects a decline of {round(abs(growth_percent),2)}% compared to the previous year."

    if top_region:
        paragraph += f" The {top_region} region led overall revenue performance."

    paragraph += " Overall performance indicates stable business operations with strategic monitoring required for sustained growth."

    return paragraph
def suggest_followups(intent):

    suggestions = {
        "ranking": [
            "Compare with last year",
            "Show revenue by region",
            "Forecast next month revenue"
        ],

        "sales": [
            "Show revenue by region",
            "Show monthly revenue trend",
            "Forecast revenue"
        ],

        "growth": [
            "Which region performs best?",
            "Compare with last year",
            "Show top products"
        ],

        "forecast": [
            "Show revenue trend",
            "Compare with last year",
            "Show top products"
        ],

        "monthly_sales": [
            "Compare with last year",
            "Show revenue by region",
            "Show top products"
        ]
    }

    return suggestions.get(intent, [])