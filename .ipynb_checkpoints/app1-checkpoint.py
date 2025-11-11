# @Author: Kevin Synagogue Panjaitan
# @Project: Crypto Dashboard 
# Requirements:
#   pip install streamlit pandas plotly

import pandas as pd
import plotly.express as px
import streamlit as st

# ------------------ PAGE CONFIG ------------------
st.set_page_config(
    page_title="Crypto Dashboard",
    layout="wide"
)

# Credit
st.markdown(
    "<p style='text-align:right; font-size:13px; opacity:0.7;'>Created by <b>Kevin Synagogue Panjaitan</b></p>",
    unsafe_allow_html=True
)

# ------------------ READ DATA ------------------
@st.cache_data
def load_crypto_data(
    path: str = "testing.csv",
    date_col: str = "Date"
) -> pd.DataFrame:
    """
    Membaca data crypto dari CSV.
    Kolom wajib: Date, Open, High, Low, Close, Volume, name
    (ticker optional)
    """
    try:
        df = pd.read_csv(path)
    except FileNotFoundError:
        st.error("Error: File 'crypto_prices.csv' tidak ditemukan.")
        st.stop()

    df.columns = df.columns.str.strip()

    # wajib ada name
    required = {"Date", "Open", "High", "Low", "Close", "Volume", "name"}
    missing = required - set(df.columns)
    if missing:
        st.error(f"Kolom wajib hilang: {', '.join(sorted(missing))}")
        st.stop()

    df[date_col] = pd.to_datetime(df[date_col], errors="coerce", utc=True)
    df["date"] = df[date_col].dt.tz_convert(None).dt.date
    df = df.sort_values(date_col).reset_index(drop=True)
    return df

df = load_crypto_data()

# ------------------ SIDEBAR FILTER ------------------
st.sidebar.header("Filter Data")

name_list = sorted(df["name"].dropna().unique())

names = st.sidebar.multiselect(
    "Pilih Nama Koin:",
    options=name_list,
    default=name_list[:10] if len(name_list) > 10 else name_list,
)

# Rentang tanggal
min_date = df["date"].min()
max_date = df["date"].max()
date_range = st.sidebar.date_input(
    "Rentang Tanggal:",
    value=(min_date, max_date),
    min_value=min_date,
    max_value=max_date
)

if isinstance(date_range, tuple) and len(date_range) == 2:
    start_date, end_date = date_range
else:
    start_date, end_date = (min_date, max_date)

# Filter
df_sel = df[
    df["name"].isin(names) &
    (df["date"] >= start_date) &
    (df["date"] <= end_date)
].copy()

if df_sel.empty:
    st.warning("Tidak ada data untuk filter tersebut.")
    st.stop()

# ------------------ MAIN PAGE ------------------
st.title(":bar_chart: Crypto Dashboard")
st.markdown("##")

# ------------------ KPI ------------------
total_volume = int(df_sel["Volume"].sum())
avg_close   = round(df_sel["Close"].mean(), 6)

daily_mean = (
    df_sel.groupby("date", as_index=False)["Close"]
    .mean()
    .sort_values("date")
)

first_close = daily_mean["Close"].iloc[0]
last_close  = daily_mean["Close"].iloc[-1]
pct_change  = ((last_close - first_close) / first_close * 100.0) if first_close != 0 else 0.0

left, mid, right = st.columns(3)

with left:
    st.subheader("Total Volume")
    st.subheader(f"{total_volume:,}")

with mid:
    st.subheader("Rata-rata Close")
    st.subheader(f"{avg_close}")

with right:
    st.subheader("% Perubahan (awal→akhir)")
    st.subheader(f"{pct_change:.2f}%")

st.markdown("---")

# ------------------ CHARTS ------------------
# Harga per waktu
fig_price = px.line(
    df_sel,
    x="Date",
    y="Close",
    color="name",
    title="<b>Harga Penutupan (Close) per Waktu</b>",
    template="plotly_white"
)
fig_price.update_layout(
    xaxis_title="Tanggal",
    yaxis_title="Harga (Close)"
)

# Volume
vol_daily = (
    df_sel.groupby(["date", "name"], as_index=False)["Volume"]
    .sum()
    .sort_values(["date", "name"])
)
fig_vol = px.bar(
    vol_daily,
    x="date",
    y="Volume",
    color="name",
    title="<b>Volume Per Hari</b>",
    template="plotly_white"
)
fig_vol.update_layout(
    xaxis_title="Tanggal",
    yaxis_title="Volume"
)

l, r = st.columns(2)
l.plotly_chart(fig_price, use_container_width=True)
r.plotly_chart(fig_vol,   use_container_width=True)

# ------------------ SUMMARY ------------------
st.markdown("---")
st.subheader("Ringkasan per Koin")

df_sel = df_sel.sort_values(["name", "Date"])

summary = (
    df_sel.groupby(["name"])
    .agg(
        first_date=("Date", "min"),
        last_date=("Date", "max"),
        first_close=("Close", "first"),
        last_close=("Close", "last"),
        avg_close=("Close", "mean"),
        min_close=("Close", "min"),
        max_close=("Close", "max"),
        total_volume=("Volume", "sum"),
    )
    .reset_index()
)

summary["pct_change_%"] = (
    (summary["last_close"] - summary["first_close"]) /
    summary["first_close"]
) * 100

st.dataframe(summary, use_container_width=True)

# ------------------ HIDE STREAMLIT DEFAULTS ------------------
hide_st_style = """
<style>
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
header {visibility: hidden;}
</style>
"""
st.markdown(hide_st_style, unsafe_allow_html=True)
