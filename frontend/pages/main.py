import pandas as pd
import streamlit as st

from pages.sidebar import render_sidebar

render_sidebar()

st.title('Главная панель GC BI')

df = pd.DataFrame({
  'Период': [1, 2, 3, 4, 5, 6],
  'Продажи, руб': [10, 20, 30, 40, 100, 80]
})

df
