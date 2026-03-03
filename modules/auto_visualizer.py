import streamlit as st
import pandas as pd
from modules.visualization import plot_bar


def auto_visualize(df):

    if df is None or df.empty:
        st.info("No data available.")
        return

    # ---- SINGLE VALUE CASE ----
    if df.shape == (1, 1):
        value = df.iloc[0, 0]

        # Safe handling
        if pd.isna(value) or value is None:
            st.warning("No data available for this query.")
            return

        if isinstance(value, (int, float)):
            st.metric("Result", f"{value:,.2f}")
        else:
            st.metric("Result", str(value))

        return

    # ---- CATEGORY + VALUE CASE ----
    if df.shape[1] >= 2:

        col1 = df.columns[0]
        col2 = df.columns[1]

        if pd.api.types.is_numeric_dtype(df[col2]):

            fig = plot_bar(df, col1, col2, f"{col2} by {col1}")
            st.pyplot(fig)
            return

    # ---- FALLBACK ----
    st.dataframe(df)
