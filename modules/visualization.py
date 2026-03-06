import matplotlib
matplotlib.use("Agg")  # Required for Streamlit Cloud

import matplotlib.pyplot as plt


# --------------------------------------------------
# BAR CHART
# --------------------------------------------------
def plot_bar(df, x_col, y_col, title="Bar Chart"):

    fig, ax = plt.subplots(figsize=(8, 5))

    if x_col not in df.columns or y_col not in df.columns:
        ax.text(0.5, 0.5, "Invalid columns", ha="center")
        return fig

    ax.bar(df[x_col], df[y_col])

    ax.set_title(title)
    ax.set_xlabel(x_col)
    ax.set_ylabel(y_col)

    ax.grid(alpha=0.3)
    plt.xticks(rotation=45)
    plt.tight_layout()

    return fig


# --------------------------------------------------
# FORECAST LINE CHART
# --------------------------------------------------
def plot_forecast(monthly_data, forecast, conf_int=None):

    fig, ax = plt.subplots(figsize=(10, 5))

    ax.plot(monthly_data.index, monthly_data.values, label="Historical")
    ax.plot(forecast.index, forecast.values, label="Forecast")

    if conf_int is not None:
        ax.fill_between(
            forecast.index,
            conf_int.iloc[:, 0],
            conf_int.iloc[:, 1],
            alpha=0.2
        )

    ax.legend()
    ax.grid(alpha=0.3)
    plt.tight_layout()

    return fig


# --------------------------------------------------
# PIE CHART
# --------------------------------------------------
def plot_pie(df, label_col, value_col):

    fig, ax = plt.subplots(figsize=(4, 4))

    if label_col not in df.columns or value_col not in df.columns:
        ax.text(0.5, 0.5, "Invalid columns", ha="center")
        return fig

    df = df[df[value_col] > 0]

    if df.empty:
        ax.text(0.5, 0.5, "No data to display", ha="center")
        return fig

    ax.pie(
        df[value_col],
        labels=df[label_col],
        autopct="%1.1f%%"
    )

    ax.set_title("Distribution")
    plt.tight_layout()

    return fig