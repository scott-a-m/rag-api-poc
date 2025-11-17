from adapters.loaders.loader_adapters import PDFLoaderAdapter

class PDFLoaderFactory:

    def create_pdf_loader(self, file_path: str):
        return PDFLoaderAdapter(file_path)

    