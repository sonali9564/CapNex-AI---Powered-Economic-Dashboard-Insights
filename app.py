import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import streamlit as st
from prophet import Prophet
from dotenv import load_dotenv

# --------------------
# 1. ENV + CONFIG
# --------------------
load_dotenv()
DATA_PATH = "data/nea_quarterly.csv"

# --------------------
# Load Dataset
# --------------------
if os.path.exists(DATA_PATH):
    df = pd.read_csv(DATA_PATH)
else:
    st.error(f"Dataset not found at {DATA_PATH}. Please place 'nea_quarterly.csv' in the 'data' folder.")
    df = pd.DataFrame()


# --------------------
# Helper Functions
# --------------------
def summarize_timeseries(df, country, indicator):
    id_cols = ["COUNTRY", "INDICATOR", "S_ADJUSTMENT", "UNIT"]
    indicator_df = df[(df["COUNTRY"].str.lower() == country.lower()) &
                      (df["INDICATOR"].str.lower() == indicator.lower())].copy()
    if indicator_df.empty:
        return f"No data available for {indicator} in {country}."

    year_cols = [c for c in indicator_df.columns if c not in id_cols]
    plot_row = indicator_df.iloc[0]  # pick first row
    values = plot_row[year_cols].values
    values = values[~pd.isna(values)]
    if len(values) == 0:
        return f"All values are missing for {indicator} in {country}."

    scale = 1e9
    values_scaled = values / scale
    trend = "increasing" if values_scaled[-1] > values_scaled[0] else "decreasing" if values_scaled[-1] < values_scaled[
        0] else "stable"
    summary = f"{indicator} for {country} shows a {trend} trend, ranging from {values_scaled.min():.2f}B to {values_scaled.max():.2f}B over the period."
    return summary


def ask(question, df=None):
    if df is None or df.empty:
        return "Dataset is empty. Cannot answer the question."

    question_lower = question.lower()
    if "summarize" in question_lower:
        words = question_lower.replace("?", "").split()
        country_candidates = df["COUNTRY"].unique()
        indicator_candidates = df["INDICATOR"].unique()

        country = next((c for c in country_candidates if c.lower() in words), None)
        indicator = next((i for i in indicator_candidates if i.lower() in words), None)

        if country and indicator:
            return summarize_timeseries(df, country, indicator)
        elif country:
            summaries = []
            for ind in df[df["COUNTRY"].str.lower() == country.lower()]["INDICATOR"].unique():
                summaries.append(summarize_timeseries(df, country, ind))
            return "\n".join(summaries)
        else:
            return "Cannot detect country or indicator from your question."
    return "I can only summarize data. Please ask to summarize a specific country and indicator."


# --------------------
# Streamlit Page
# --------------------
page = st.sidebar.selectbox(
    "**Navigation Bar**",
    ["🔮 Dashboard", "📈 Forecasting", "⚖️ Capital Mix Optimization Analytics", "🤖 Ask CapNex"]
)

# --------------------
# Dashboard
# --------------------
if page == "🔮 Dashboard":
    st.markdown("""
    <div style='text-align: center;'>
        <h1 style='font-size:60px;'>📊 CapNex</h1>
        <h3 style='font-size:28px; font-weight: bold;'>Economic Trends at a Glance — Turning Data into Decisions</h3>
    </div>
    """, unsafe_allow_html=True)
    if df.empty:
        st.warning("Dataset is empty. Please upload the CSV in 'data/nea_quarterly.csv'.")
    else:
        st.subheader("First 5 rows of the dataset")
        st.dataframe(df.head())

        st.subheader("Filter by Country")
        countries = sorted(df["COUNTRY"].unique())
        country = st.selectbox("Select Country", countries)
        country_df = df[df["COUNTRY"].str.lower() == country.lower()].copy()
        st.dataframe(country_df)

        st.subheader("Select Indicator to Chart")
        indicators = sorted(country_df["INDICATOR"].unique())
        selected_indicator = st.selectbox("Indicator", indicators)

        indicator_df = country_df[country_df["INDICATOR"] == selected_indicator].copy()
        id_cols = ["COUNTRY", "INDICATOR", "S_ADJUSTMENT", "UNIT"]
        year_cols = [c for c in indicator_df.columns if c not in id_cols]

        if st.button("Generate Chart"):
            plot_row = indicator_df.iloc[0]
            fig, ax = plt.subplots(figsize=(12, 5))
            ax.plot(year_cols, plot_row[year_cols].values, marker='o')
            ax.set_xlabel("Period")
            ax.set_ylabel("Value")
            ax.set_title(f"{selected_indicator} for {country}")
            plt.xticks(rotation=90)
            st.pyplot(fig)

            summary = summarize_timeseries(df, country, selected_indicator)
            st.subheader("💡 AI Recommendation / Chart Summary")
            st.write(summary)

# --------------------
# Forecasting
# --------------------
elif page == "📈 Forecasting":
    st.title("**📈 Forecasting**")
    country = st.text_input("**Enter Name of Country**")
    indicators = df["INDICATOR"].unique().tolist() if not df.empty else []
    indicator = st.selectbox("Select Indicator", indicators)
    horizon = st.slider("Forecast horizon (quarters)", 1, 8, 4)

    if st.button("Run Forecast") and country and indicator and not df.empty:
        indicator_df = df[(df["COUNTRY"].str.lower() == country.lower()) &
                          (df["INDICATOR"].str.lower() == indicator.lower())].copy()
        id_cols = ["COUNTRY", "INDICATOR", "S_ADJUSTMENT", "UNIT"]
        year_cols = [c for c in indicator_df.columns if c not in id_cols]

        ts = indicator_df.melt(id_vars=id_cols, value_vars=year_cols, var_name="ds", value_name="y")
        ts["y"] = pd.to_numeric(ts["y"], errors='coerce')


        def quarter_to_date(q):
            try:
                y, qn = q.split("-Q")
                month = (int(qn) - 1) * 3 + 1
                return f"{y}-{month:02d}-01"
            except:
                return q


        ts["ds"] = pd.to_datetime(ts["ds"].astype(str).apply(quarter_to_date))

        ts = ts.groupby("ds")["y"].mean().reset_index()  # handle multiple rows
        ts["y"] = ts["y"] / 1e9  # scale to billions

        m = Prophet()
        m.fit(ts)
        future = m.make_future_dataframe(periods=horizon, freq="Q")
        forecast = m.predict(future)

        fig = m.plot(forecast)
        st.pyplot(fig)

        forecast_values = forecast['yhat'].tail(horizon).values
        trend = "increasing" if forecast_values[-1] > forecast_values[0] else "decreasing" if forecast_values[-1] < \
                                                                                              forecast_values[
                                                                                                  0] else "stable"
        forecast_summary = f"Forecast for {indicator} in {country} shows a {trend} trend over the next {horizon} quarters, with predicted values ranging from {forecast_values.min():.2f}B to {forecast_values.max():.2f}B."
        st.subheader("💡 AI Summary")
        st.write(forecast_summary)

# --------------------
# Capital Mix Optimization Analytics
# --------------------
elif page == "⚖️ Capital Mix Optimization Analytics":
    st.title("**⚙️ Capital Mix Optimization Analytics**")
    country = st.text_input("**Enter Name of Country**")
    capital = st.number_input("Working capital (M USD)", 1.0, 1000.0, 100.0)
    c = st.slider("Cash %", 0, 100, 30)
    inv = st.slider("Inventory %", 0, 100, 30)
    rec = st.slider("Receivables %", 0, 100, 20)
    pay = st.slider("Payables %", 0, 100, 20)

    if c + inv + rec + pay != 100:
        st.warning("Allocations must sum to 100%")
    else:
        alloc = {
            "Cash": round(capital * c / 100, 2),
            "Inventory": round(capital * inv / 100, 2),
            "Receivables": round(capital * rec / 100, 2),
            "Payables": round(capital * pay / 100, 2)
        }
        st.subheader("**📊 Allocated Amounts (M USD)**")
        st.table(pd.DataFrame.from_dict(alloc, orient="index", columns=["M USD"]))

        fig, ax = plt.subplots(figsize=(6, 4))
        ax.bar(alloc.keys(), alloc.values(), color='skyblue')
        ax.set_ylabel("M USD")
        ax.set_title(f"{country} Allocation")
        st.pyplot(fig)

        alloc_summary = f"""
For {country} with working capital {capital}M USD:
- Cash: {alloc['Cash']}M
- Inventory: {alloc['Inventory']}M
- Receivables: {alloc['Receivables']}M
- Payables: {alloc['Payables']}M

Recommendations:
- Ensure cash buffer is sufficient for short-term obligations.
- Optimize inventory to reduce holding costs while avoiding stockouts.
- Monitor receivables to improve cash flow.
- Consider negotiating payables terms to maintain liquidity.
"""
        st.subheader("💡 AI Recommendation")
        st.write(alloc_summary)

# --------------------
# Ask CapNex
# --------------------
elif page == "🤖 Ask CapNex":
    st.title("**💬 Ask CapNex — Your Economic AI Assistant**")
    st.subheader("Ask anything about your economic dataset and get smart insights!")
    if "qna_history" not in st.session_state:
        st.session_state.qna_history = []

    q = st.text_area("Your question here:")
    if st.button("Ask") and q.strip():
        ans = ask(q, df)
        st.session_state.qna_history.append({"Q": q, "A": ans})

    for idx, qa in enumerate(st.session_state.qna_history, start=1):
        st.markdown(f"**Q{idx}:** {qa['Q']}")
        st.markdown(f"**A{idx}:** {qa['A']}")
