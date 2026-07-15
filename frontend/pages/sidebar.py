import streamlit as st


def render_sidebar():
    """Рендерит боковую панель с отчетами."""
    with st.sidebar:
        st.title('Отчёты')

        st.subheader('Продажи')
        if st.button('ОПТ', width='stretch', key='rep_sales_opt',):
            st.switch_page('pages/reports_sales.py')

        st.subheader('Закуп')
        if st.button('Закуп', width='stretch', key='rep_purchase'):
            st.switch_page('pages/reports_purchase.py')
