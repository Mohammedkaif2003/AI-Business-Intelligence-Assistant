import streamlit as st
import pandas as pd
from modules.visualization import plot_bar, plot_pie


def auto_visualize(df):

    if df is None or df.empty:
        st.info("No data available.")
        return

    # --------------------------
    # SINGLE VALUE
    # --------------------------
    if df.shape == (1, 1):
        value = df.iloc[0, 0]

        if pd.isna(value):
            st.warning("No data available.")
            return

        st.metric("Result", f"{value:,.2f}")
        return

    # --------------------------
    # TIME SERIES
    # --------------------------
    if "Date" in df.columns or "Month" in df.columns:

        x = df.columns[0]
        y = df.columns[1]

        st.line_chart(df.set_index(x)[y])
        return

    # --------------------------
    # PIE CHART CASE
    # --------------------------
    if "Region" in df.columns or "Contribution_%" in df.columns:

        col1 = df.columns[0]
        col2 = df.columns[1]

        fig = plot_pie(df, col1, col2)
        st.pyplot(fig)
        return

    # --------------------------
    # DEFAULT BAR CHART
    # --------------------------
    if df.shape[1] >= 2:

        col1 = df.columns[0]
        col2 = df.columns[1]

        if pd.api.types.is_numeric_dtype(df[col2]):
            fig = plot_bar(df, col1, col2, f"{col2} by {col1}")
            st.pyplot(fig)
            return

    # --------------------------
    # FALLBACK
    # --------------------------
    st.dataframe(df)
