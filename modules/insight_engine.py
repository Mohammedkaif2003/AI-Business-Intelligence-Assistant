import pandas as pd


def generate_business_insight(df):

    if df is None or df.empty:
        return "No data available for insight generation."

    insights = []

    # Detect numeric column
    numeric_cols = df.select_dtypes(include="number").columns

    if len(numeric_cols) == 0:
        return "Dataset does not contain numeric values."

    metric = numeric_cols[0]

    # Top performer
    top_row = df.sort_values(metric, ascending=False).iloc[0]
    bottom_row = df.sort_values(metric).iloc[0]

    insights.append(
        f"🏆 Top performer: **{top_row[0]}** with {top_row[metric]:,.0f}."
    )

    insights.append(
        f"📉 Lowest performer: **{bottom_row[0]}** with {bottom_row[metric]:,.0f}."
    )

    # Concentration risk
    total = df[metric].sum()
    share = (top_row[metric] / total) * 100

    if share > 50:
        insights.append(
            f"⚠ High concentration risk: top entity contributes {share:.1f}% of total."
        )

    elif share > 35:
        insights.append(
            f"⚠ Moderate dependency detected: top entity contributes {share:.1f}%."
        )

    # Performance gap
    gap = top_row[metric] / bottom_row[metric] if bottom_row[metric] != 0 else 0

    if gap > 4:
        insights.append(
            "⚖ Large performance gap between top and bottom performers."
        )

    return " ".join(insights)