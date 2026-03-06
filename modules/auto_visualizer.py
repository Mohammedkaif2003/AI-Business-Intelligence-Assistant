import streamlit as st
import pandas as pd


def auto_visualize(df):

    if df is None or df.empty:
        return

    numeric_cols = df.select_dtypes(include="number").columns.tolist()
    cat_cols = df.select_dtypes(include="object").columns.tolist()

    # ---------------- BAR CHART ----------------
    if len(cat_cols) > 0 and len(numeric_cols) > 0:

        st.subheader("📊 Bar Chart")

        try:
            st.bar_chart(df.set_index(cat_cols[0])[numeric_cols[0]])
        except:
            st.bar_chart(df[numeric_cols])

    # ---------------- LINE CHART ----------------
    if "Month" in df.columns and len(numeric_cols) > 0:

        st.subheader("📈 Line Chart")

        try:
            st.line_chart(df.set_index("Month")[numeric_cols[0]])
        except:
            st.line_chart(df[numeric_cols])

    # ---------------- PIE CHART ----------------
    if len(cat_cols) > 0 and len(numeric_cols) > 0:

        st.subheader("🥧 Pie Chart")

        try:
            pie_data = df.set_index(cat_cols[0])[numeric_cols[0]]
            st.pyplot(pie_data.plot.pie(autopct="%1.1f%%").get_figure())
        except:
            pass

    # ---------------- DATA TABLE ----------------
    st.subheader("📋 Data Table")
    st.dataframe(df)