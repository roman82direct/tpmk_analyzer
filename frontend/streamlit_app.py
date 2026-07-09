import httpx
import streamlit as st

API_UPLOAD_URL = 'http://localhost:8000/api/v1/upload-data/'

st.title('TPMK Analyzer')

if st.button('Загрузить данные'):
    with st.spinner('Идёт загрузка...'):
        try:
            with httpx.Client(timeout=30) as client:
                response = client.post(API_UPLOAD_URL)
                response.raise_for_status()
                st.success('Готово')
                st.json(response.json())
        except httpx.HTTPError as error:
            st.error(f'Ошибка загрузки: {error}')
