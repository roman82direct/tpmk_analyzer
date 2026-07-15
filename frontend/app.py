import httpx
import streamlit as st

API_UPLOAD_URL = 'http://localhost:8000/api/v1/upload-data/'

# st.title('TPMK Analyzer')

# if st.button('Загрузить данные'):
#     with st.spinner('Идёт загрузка...'):
#         try:
#             with httpx.Client(timeout=30) as client:
#                 response = client.post(API_UPLOAD_URL)
#                 response.raise_for_status()
#                 st.success('Готово')
#                 st.json(response.json())
#         except httpx.HTTPError as error:
#             st.error(f'Ошибка загрузки: {error}')

main_page = st.Page('pages/main.py', title='Главная')
processing_page = st.Page('pages/processing.py', title='Обработка')
login_page = st.Page('pages/login.py', title='Войти в систему')
register_page = st.Page('pages/register.py', title='Регистрация')
sales_reports_page = st.Page('pages/reports_sales.py',
                             title='Отчеты по продажам')
purchase_reports_page = st.Page('pages/reports_purchase.py',
                                title='Отчеты по закупкам')

st.set_page_config(page_title='TPMK analyzer', layout='wide')

nav = st.navigation(
    {
        'Главная': [main_page],
        'Обработка': [processing_page],
        'Отчёты': [sales_reports_page, purchase_reports_page],
        'Доступ': [login_page, register_page],
    },
    position='top',
)

nav.run()
