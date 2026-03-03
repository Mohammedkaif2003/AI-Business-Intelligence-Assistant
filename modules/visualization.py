def plot_bar(data, title):
    import matplotlib.pyplot as plt
    
    fig, ax = plt.subplots()
    data.plot(kind='bar', ax=ax)
    ax.set_title(title)
    ax.set_ylabel("Revenue")
    ax.set_xlabel("")
    
    return fig


def plot_forecast(history, forecast):
    import matplotlib.pyplot as plt
    
    fig, ax = plt.subplots()
    
    history.plot(ax=ax, label="Historical Revenue")
    forecast.plot(ax=ax, label="Forecast", color="red")
    
    ax.legend()
    ax.set_title("Revenue Forecast")
    
    return fig
import matplotlib.pyplot as plt

def plot_pie(df, title):
    fig, ax = plt.subplots()
    ax.pie(df["Total_Revenue"], labels=df["Product"], autopct='%1.1f%%')
    ax.set_title(title)
    return fig