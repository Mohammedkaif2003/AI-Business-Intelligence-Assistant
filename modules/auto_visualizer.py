import streamlit as st
import pandas as pd
import plotly.express as px


def auto_visualize(df):

    if df is None or df.empty:
        return

    numeric_cols = df.select_dtypes(include="number").columns.tolist()
    cat_cols = df.select_dtypes(include="object").columns.tolist()

    st.subheader("📊 Visual Analysis")

    # ---------- BAR CHART ----------
    if len(cat_cols) > 0 and len(numeric_cols) > 0:

        fig = px.bar(
            df,
            x=cat_cols[0],
            y=numeric_cols[0],
            color=cat_cols[0],
            title=f"{numeric_cols[0]} by {cat_cols[0]}"
        )

        st.plotly_chart(fig, use_container_width=True)

    # ---------- LINE CHART ----------
    time_cols = ["Month", "Date", "Year"]

    for col in time_cols:

        if col in df.columns and len(numeric_cols) > 0:

            fig = px.line(
                df,
                x=col,
                y=numeric_cols[0],
                markers=True,
                title=f"{numeric_cols[0]} Trend"
            )

            st.plotly_chart(fig, use_container_width=True)

            break

    # ---------- PIE CHART ----------
    if len(cat_cols) > 0 and len(numeric_cols) > 0:

        if len(df) <= 10:

            fig = px.pie(
                df,
                names=cat_cols[0],
                values=numeric_cols[0],
                title=f"{numeric_cols[0]} Distribution"
            )

            st.plotly_chart(fig, use_container_width=True)

    # ---------- DATA TABLE ----------
    st.subheader("📋 Data Table")
    st.dataframe(df)