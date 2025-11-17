from langchain_text_splitters import CharacterTextSplitter, RecursiveCharacterTextSplitter

class RecursiveCharacterSplitterAdapter:
    def __init__(self, chunk_size=1000, chunk_overlap=50):
        self.splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size, chunk_overlap=chunk_overlap
        )

    def split_documents(self, docs):
        return self.splitter.split_documents(docs)

class CharacterSplitterAdapter:
    def __init__(self, chunk_size=1000, chunk_overlap=50):
        self.splitter = CharacterTextSplitter(
            chunk_size=chunk_size, chunk_overlap=chunk_overlap
        )

    def split_documents(self, docs):
        return self.splitter.split_documents(docs)