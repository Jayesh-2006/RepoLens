from importlib_metadata import metadata
from rank_bm25 import BM25Okapi

from models import RetrievedDocument
from retrievers.base_retriever import BaseRetriever

from langchain_core.documents import Document
import re

def tokenize(text):
    return re.findall(r"\w+", text.lower())

class BM25Retriever(BaseRetriever):

    def __init__(self, vector_store):

        data = vector_store.get_documents()

        self.documents = data["documents"]
        self.metadatas = data["metadatas"]

        corpus = [tokenize(doc) for doc in self.documents]

        self.bm25 = BM25Okapi(corpus)

    def retrieve(self, query: str, top_k: int = 20) -> list[RetrievedDocument]:

        scores = self.bm25.get_scores(tokenize(query))

        ranked = sorted(
            enumerate(scores),
            key=lambda x: x[1],
            reverse=True
        )[:top_k]

        return [
            RetrievedDocument(
                    page_content=self.documents[idx],
                    source=self.metadatas[idx]["source"],
                    chunk_id=self.metadatas[idx]["chunk_id"],
                    extension=self.metadatas[idx]["extension"],
                    retriever="bm25",
                    rank=rank + 1,
                    symbol=self.metadatas[idx].get("symbol"),
                    chunk_type=self.metadatas[idx].get("chunk_type")
            )
            for rank, (idx, _) in enumerate(ranked)
        ]