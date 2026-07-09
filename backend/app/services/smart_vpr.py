# Анализ пересекающихся аналогов в двух файлах, когда в прайсе конкурента
# код поставщика в отдельной колонке, а в tpmk код поставщика зашит
# в наименование товара.
# Сохраняет новый файл, добавляя в файл конкурента наш артикул,
# наименование и СС по строкам, где артикул поставщика совпадает.

import logging
from pathlib import Path

import pandas as pd


logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


BASE_DIR = Path('xls')
SPECTORG_FILE = BASE_DIR / 'spectorg.xlsx'
TPMK_FILE = BASE_DIR / 'tpmk.xlsx'

SPECTORG_CACHE = Path('spectorg.pkl')
TPMK_CACHE = Path('tpmk.pkl')

OUT_FILE = BASE_DIR / 'spectorg_gc.xlsx'


def load_df(xlsx_path: Path, cache_path: Path, header: int) -> pd.DataFrame:
    if cache_path.exists():
        logger.info('Загружен %s из кэша', cache_path.name)
        return pd.read_pickle(cache_path)

    df = pd.read_excel(xlsx_path, header=header)
    df.to_pickle(cache_path)
    logger.info('Загружен %s и сохранён в кэш', xlsx_path.name)
    return df


if __name__ == '__main__':
    st_df = load_df(SPECTORG_FILE, SPECTORG_CACHE, header=5)
    gc_df = load_df(TPMK_FILE, TPMK_CACHE, header=1)

    st_df.columns = st_df.columns.astype(str).str.strip()
    gc_df.columns = gc_df.columns.astype(str).str.strip()

    if 'Артикул' not in st_df.columns:
        raise KeyError(f'В spectorg нет колонки Артикул. '
                       f'Есть: {st_df.columns.tolist()}')

    if 'Товар' not in gc_df.columns:
        raise KeyError(f'В tpmk нет колонки Товар. '
                       f'Есть: {gc_df.columns.tolist()}')

    code_col = 'Код' if 'Код' in gc_df.columns else None
    if code_col is None:
        raise KeyError(f'В tpmk нет колонки Код. '
                       f'Есть: {gc_df.columns.tolist()}')

    st_df['Артикул'] = st_df['Артикул'].astype(str).str.strip()
    gc_df['Товар'] = gc_df['Товар'].astype(str)

    mapping = {}
    matched = 0
    missed = []

    for art in st_df['Артикул'].dropna().unique():
        mask = gc_df['Товар'].str.contains(art, na=False, regex=False)
        rows = gc_df.loc[mask, ['Код', 'Товар', 'Себ., руб.']]

        if not rows.empty:
            first_row = rows.iloc[0]
            mapping[art] = (first_row['Код'], first_row['Товар'],
                            first_row['Себ., руб.'])
            matched += 1
            logger.info('Совпадение: %s -> %s', art, first_row['Код'])
        else:
            mapping[art] = (pd.NA, pd.NA, pd.NA)
            missed.append(art)
            logger.warning('Не найдено совпадение для артикула: %s', art)

        st_df[['Код_из_tpmk', 'Товар_из_tpmk', 'Цена_из_tpmk']] = (
            st_df['Артикул']
            .map(mapping)
            .apply(pd.Series)
        )

        st_df.to_excel(OUT_FILE, index=False)

    logger.info('Результат сохранён в %s', OUT_FILE)
    logger.info('Всего артикулов: %s', len(mapping))
    logger.info('Совпало: %s', matched)
    logger.info('Не найдено: %s', len(missed))
