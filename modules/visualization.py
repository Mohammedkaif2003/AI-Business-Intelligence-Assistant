import matplotlib
matplotlib.use("Agg")

import matplotlib.pyplot as plt


def plot_bar(df, x_col, y_col, title="Bar Chart"):

    fig, ax = plt.subplots(figsize=(8, 5))

    ax.bar(df[x_col], df[y_col])
    ax.set_title(title)
    ax.set_xlabel(x_col)
    ax.set_ylabel(y_col)
    ax.grid(alpha=0.3)

    plt.xticks(rotation=45)
    plt.tight_layout()

    return fig


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

    return fig


def plot_pie(df, label_col, value_col):

    fig, ax = plt.subplots(figsize=(6, 6))

    ax.pie(df[value_col], labels=df[label_col], autopct="%1.1f%%")
    ax.set_title("Distribution")

    return fig
