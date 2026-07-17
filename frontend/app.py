import sys
from pathlib import Path

import httpx
import streamlit as st

# для корректного импорта st_settings 
ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from frontend.config.st_settings import st_settings

# API_UPLOAD_URL = f'{st_settings.api_base_url}upload-data/'

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

st.set_page_config(page_title=f'{st_settings.app_name}', layout='wide')

nav = st.navigation(
    {
        'Главная': [main_page],
        'Обработка': [processing_page],
        'Отчёты': [sales_reports_page, purchase_reports_page],
        'Доступ': [login_page, register_page],
    },
    position='top',
)

st_settings.app_name
st_settings.app_description

nav.run()
