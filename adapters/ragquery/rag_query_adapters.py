from langchain_ollama import ChatOllama
from services.vector_db_service import VectorDbService
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough

class OllamaRagQueryAdapter:
    def __init__(self, vector_db_service: VectorDbService, llm_model):
            self.vector_db_service = vector_db_service
            self.llm_model = llm_model

    def handle_rag_query(self, user_input: str) -> str:
        if not user_input:
            return None

        llm = ChatOllama(model=self.llm_model)

        retriever = self.vector_db_service.get_retriever()

        prompt = ChatPromptTemplate.from_template(
            """Answer the question based ONLY on the following context. The context ends after the following character sequence:
            {context}
            Question: {question}
            """
        )

        chain = (
            {"context": retriever, "question": RunnablePassthrough()}
            | prompt
            | llm
            | StrOutputParser()
        )

        return chain.invoke(user_input)
