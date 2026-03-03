import streamlit as st
import pandas as pd
from modules.visualization import plot_bar

def auto_visualize(df):

    if df is None or df.empty:
        st.info("No data available.")
        return

    # If single numeric value
    if df.shape == (1, 1):
        value = df.iloc[0, 0]
        st.metric("Result", f"{value:,}")
        return

    # If two columns (category + number)
    if df.shape[1] == 2:
        col1, col2 = df.columns

        if pd.api.types.is_numeric_dtype(df[col2]):
            fig = plot_bar(df, col1, col2, f"{col2} by {col1}")
            st.pyplot(fig)
            return

    # Fallback
    st.dataframe(df)
