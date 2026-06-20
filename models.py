"""
models.py

Shared dataclasses used across RepoLens.
"""

from dataclasses import dataclass
from langchain_core.documents import Document


@dataclass
class RetrievedDocument:

    page_content: str

    source: str

    chunk_id: int

    extension: str

    retriever: str
    symbol: str | None = None
    chunk_type: str | None = None
    rank: int | None = None

    score: float | None = None
    @classmethod
    def from_document(cls,document: Document,retriever: str = "graph",score: float = 0.0):

        metadata = document.metadata

        return cls(
            page_content=document.page_content,
            source=metadata["source"],
            chunk_id=metadata["chunk_id"],
            extension=metadata["extension"],
            retriever=retriever,
            symbol=metadata.get("symbol"),
            chunk_type=metadata.get("chunk_type"),
            score=score
        )




@dataclass
class SearchResponse:

    query: str

    results: list[RetrievedDocument]


@dataclass
class ChatResponse:

    query: str

    answer: str

    sources: list[RetrievedDocument]

@dataclass
class CodeChunk:
    name: str
    type: str
    source: str
    content: str | None = None