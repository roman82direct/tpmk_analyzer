import pandas as pd
import plotly.express as px
import streamlit as st

st.set_page_config(page_title="Мини-дашборд", page_icon="📊", layout="wide")

df = pd.DataFrame(
    {
        "date": pd.date_range("2026-07-01", periods=10, freq="D"),
        "category": ["A", "B", "A", "C", "B", "A", "C", "B", "A", "C"],
        "sales": [120, 95, 150, 80, 110, 170, 90, 130, 160, 100],
        "region": ["Moscow", "SPb", "Moscow", "Kazan", "SPb", "Moscow", "Kazan", "SPb", "Moscow", "Kazan"],
    }
)

st.sidebar.header("Фильтры")
category = st.sidebar.selectbox("Категория", ["Все"] + sorted(df["category"].unique().tolist()))
region = st.sidebar.selectbox("Регион", ["Все"] + sorted(df["region"].unique().tolist()))
min_sales = int(df["sales"].min())
max_sales = int(df["sales"].max())
sales_range = st.sidebar.slider("Продажи", min_sales, max_sales, (min_sales, max_sales))

filtered = df.copy()
if category != "Все":
    filtered = filtered[filtered["category"] == category]
if region != "Все":
    filtered = filtered[filtered["region"] == region]
filtered = filtered[
    (filtered["sales"] >= sales_range[0]) & (filtered["sales"] <= sales_range[1])
]

st.title("Мини-дашборд продаж")
c1, c2, c3 = st.columns(3)
c1.metric("Строк", len(filtered))
c2.metric("Сумма продаж", int(filtered["sales"].sum()) if not filtered.empty else 0)
c3.metric("Среднее", round(filtered["sales"].mean(), 1) if not filtered.empty else 0)

left, right = st.columns([2, 1])

with left:
    fig = px.line(filtered, x="date", y="sales", color="category", markers=True, title="Продажи по датам")
    st.plotly_chart(fig, use_container_width=True)

with right:
    st.subheader("Таблица")
    st.dataframe(filtered, use_container_width=True)

st.subheader("Сводка по категориям")
summary = filtered.groupby("category", as_index=False)["sales"].sum()
st.bar_chart(summary, x="category", y="sales")
