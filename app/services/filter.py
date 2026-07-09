import logging

import pandas as pd


logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger(__name__)

# table = pd.DataFrame({'A': [1, 2, 3], 'B': ['a', 'b', 'c']})

FILTER_CODE_COLUMN = 'Код'
FILTER_CODE_VALUE = '8'
FILTER_GROUP_COLUMN = 'Группа 1'
FILTER_GROUP_VALUE = 'Посуда и кухонные принадлежности'
FILTERED_FILE = f'tpmk_{FILTER_CODE_VALUE}00.xlsx'


# ETL‑операции (Extract–Transform–Load)

# Чтение и кэширование в pickle (Extract)
try:
    df = pd.read_pickle('tpmk_big.pkl')            # Загрузка из кэша
    logger.debug('Загружено из кэша')
except FileNotFoundError:
    df = pd.read_excel('tpmk_big.xlsx', header=2)  # Первое чтение
    df.to_pickle('tpmk_big.pkl')                   # Сохранение кэша
    logger.info('Файл прочитан и закэширован')


# print(df.columns.tolist())

# Transform
# выводим списком уникальные значения по колонке без пустых
print(df[FILTER_GROUP_COLUMN].dropna().unique())

# фильтруем данные по артикулу с 8 и по группе 'Посуда...'
mask = (
    df[FILTER_CODE_COLUMN]
    .astype(str).str.startswith(FILTER_CODE_VALUE)
) & (
    df[FILTER_GROUP_COLUMN]
    .astype(str).eq(FILTER_GROUP_VALUE))

df_filtered = df[mask]

# сохраняем в новый файл (Load)
df_filtered.to_excel(FILTERED_FILE, index=False)
