import streamlit as st
import pandas as pd


def auto_visualize(df):

    if df is None or df.empty:
        return

    numeric_cols = df.select_dtypes(include="number").columns.tolist()
    cat_cols = df.select_dtypes(include="object").columns.tolist()

    st.subheader("📊 Visual Analysis")

    # ---------------- BAR CHART ----------------
    if len(cat_cols) > 0 and len(numeric_cols) > 0:

        try:
            st.bar_chart(df.set_index(cat_cols[0])[numeric_cols[0]])
        except:
            st.bar_chart(df[numeric_cols])

    # ---------------- LINE CHART (time data) ----------------
    time_cols = ["Month", "Date", "Year", "Quarter"]

    for col in time_cols:
        if col in df.columns and len(numeric_cols) > 0:
            try:
                st.line_chart(df.set_index(col)[numeric_cols[0]])
                break
            except:
                pass

    # ---------------- PIE CHART (limit categories) ----------------
    if len(cat_cols) > 0 and len(numeric_cols) > 0:

        try:
            pie_data = df.set_index(cat_cols[0])[numeric_cols[0]]

            if len(pie_data) <= 10:
                st.pyplot(pie_data.plot.pie(autopct="%1.1f%%").get_figure())
        except:
            pass

    # ---------------- DATA TABLE ----------------
    st.subheader("📋 Data Table")
    st.dataframe(df)