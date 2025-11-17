from protocols.protocols import RagQueryHandler

class RagQueryService:
    def __init__(self, rag_query_handler: RagQueryHandler):
        self.rag_query_handler = rag_query_handler

    def handle_query(self, user_input):
        return self.rag_query_handler.handle_rag_query(user_input)