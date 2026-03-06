import pandas as pd


def generate_business_insight(df):

    if df is None or df.empty:
        return "No data available for insight generation."

    insights = []

    numeric_cols = df.select_dtypes(include="number").columns.tolist()

    if len(numeric_cols) == 0:
        return "Dataset does not contain numeric values."

    metric = numeric_cols[0]
    entity_col = df.columns[0]

    df_sorted = df.sort_values(metric, ascending=False)

    top_row = df_sorted.iloc[0]
    bottom_row = df_sorted.iloc[-1]

    # Top performer
    insights.append(
        f"🏆 Top performer: **{top_row[entity_col]}** with {top_row[metric]:,.0f}."
    )

    # Lowest performer
    insights.append(
        f"📉 Lowest performer: **{bottom_row[entity_col]}** with {bottom_row[metric]:,.0f}."
    )

    # Concentration analysis
    total = df[metric].sum()

    if total > 0:
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
    if bottom_row[metric] != 0:
        gap = top_row[metric] / bottom_row[metric]

        if gap > 4:
            insights.append(
                "⚖ Large performance gap between top and bottom performers."
            )

    return " ".join(insights)