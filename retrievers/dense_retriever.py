"""
Dense Retriever module for RAG system. 
This module is responsible for retrieving relevant documents from the vector database 
based on the query embedding. It uses the HuggingFaceEmbeddings model to generate 
embeddings for the query and retrieves the most relevant documents from the Chroma vector store.
"""

from indexing.vectordb import VectorStore
from retrievers.base_retriever import BaseRetriever
from models import RetrievedDocument


class DenseRetriever(BaseRetriever):

    def __init__(self, vector_store : VectorStore):
        self.vector_store = vector_store

    def retrieve(self, query: str, top_k: int = 10) -> list[RetrievedDocument]:
        retriever = self.vector_store.as_retriever(
            search_type = "mmr",
            search_kwargs={"k": top_k, "fetch_k": top_k * 5}
            )
        results = retriever.invoke(query)

        return [RetrievedDocument(
            page_content=doc.page_content,
            source=doc.metadata["source"],
            chunk_id=doc.metadata["chunk_id"],
            extension=doc.metadata["extension"],  
            retriever="dense",
            symbol=doc.metadata.get("symbol"),
            chunk_type=doc.metadata.get("chunk_type")
        ) for doc in results]
    
    