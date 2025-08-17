import streamlit as st
import pandas as pd

from src.loader import (
    format_analysis,
    get_monthly_analysis,
    load_stocks_from_data_dir,
)
from src.plots import (
    generate_heatmap,
    generate_monthly_avg_barchart,
)

st.set_page_config(page_title="Price Action Dashboard", layout="wide")


# --- Load full stocks DataFrame ---
@st.cache_data(ttl=60 * 60)
def load_data():
    return load_stocks()

stocks_df = load_data()  # This should have columns: ["Name", "Ticker", "Sector", ...]


# --- Sidebar filters ---
st.sidebar.title("Filters")

# 1) Sector filter
sectors = stocks_df["Sector"].unique()
selected_sector = st.sidebar.selectbox("Choose a sector:", sorted(sectors))

# 2) Stock filter (based on selected sector)
sector_stocks = stocks_df[stocks_df["Sector"] == selected_sector]
selected_stock_name = st.sidebar.selectbox("Choose a stock:", sector_stocks["Name"].unique())

# 3) Get ticker of chosen stock
selected_stock_ticker = sector_stocks.loc[
    sector_stocks["Name"] == selected_stock_name, "Ticker"
].values[0]


# --- Main page ---
st.title("Price Action Dashboard")
st.write(f"### Selected Stock: **{selected_stock_name}** `({selected_stock_ticker})`")

tab1, tab2, tab3 = st.tabs(["📄 Price Action Data", "🔥 Heatmap", "📊 Bar Charts"])


@st.cache_data(ttl=60 * 60)
def get_formatted_table(stock: str):
    return format_analysis(get_monthly_analysis(stock))


with tab1:
    st.subheader("Price Action DataFrame")
    analysis = get_formatted_table(selected_stock_ticker)
    st.dataframe(analysis)

with tab2:
    st.subheader("Heatmap")
    fig = generate_heatmap(selected_stock_ticker)
    fig.update_layout(
        height=600,
        font=dict(size=16),
    )
    st.plotly_chart(fig)

with tab3:
    st.subheader("Bar Chart")
    fig = generate_monthly_avg_barchart(selected_stock_ticker)
    st.plotly_chart(fig, use_container_width=True, config={"scrollZoom": False})

