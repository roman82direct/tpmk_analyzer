from backend.app.services.etl.extractors.xlsx import XlsxExtractor
from backend.app.config.settings import backend_settings


class PipelineETL:
    """Класс сценария загрузки, обработки, сохранения в БД данных."""

    def __init__(
            self,
            extractor: XlsxExtractor,
            transformer=None,
            loader=None
    ) -> None:
        self.extractor = extractor
        self.transformer = transformer
        self.loader = loader

    def run(self):
        return self.extractor.extract()


if __name__ == '__main__':
    file_path = backend_settings.storage_input_dir / 'tpmk_new_01.01.2001.xlsx'

    extractor = XlsxExtractor(file_path)
    pipeline = PipelineETL(extractor)

    data = pipeline.run()
    print(f'{data[5]}')



#  python -m backend.app.services.etl.pipline
