from langchain_community.document_loaders import PyPDFLoader, TextLoader

class PDFLoaderAdapter:
    def __init__(self, file_path: str):
        self.loader = PyPDFLoader(file_path)

    def load(self):
        return self.loader.load()

class TextLoaderAdapter:
    def __init__(self, file_path: str):
        self.loader = TextLoader(file_path)

    def load(self):
        return self.loader.load()
