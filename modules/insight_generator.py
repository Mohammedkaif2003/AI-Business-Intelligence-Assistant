def generate_insight(df, metric="revenue"):
    if metric not in df.columns:
        return "No insight available."

    top = df.sort_values(metric, ascending=False).iloc[0]
    bottom = df.sort_values(metric).iloc[0]
    

    insight = f"""
Top performer: {top['product']} with {top[metric]} revenue.
Lowest performer: {bottom['product']} with {bottom[metric]} revenue.
"""

    return insight