from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings

from langchain_core.documents import Document
from dotenv import load_dotenv
import tqdm

load_dotenv()

class VectorStore:
    def __init__(self,collection_name: str = "repo_chunks", embedding_model=None, db=None,device : str = "cpu"):
        self.embedding_model = embedding_model or HuggingFaceEmbeddings(model_name="BAAI/bge-m3",model_kwargs={"device": device},encode_kwargs={"batch_size": 8})
        self.collection_name = collection_name
        self.db = db or Chroma(
            collection_name=collection_name,
            embedding_function=self.embedding_model,
            persist_directory="data/chroma_db"
        )
    
    def add_documents(self, chunks):

        ids = [
            f"{doc.metadata['source']}:{doc.metadata['chunk_id']}"
            for doc in chunks
        ]

        batch_size = 2000

        for i in tqdm.tqdm(range(0, len(chunks), batch_size), desc="Adding documents"):

            self.db.add_documents(documents=chunks[i:i+batch_size],ids=ids[i:i+batch_size])

            print(f"Added {min(i+batch_size,len(chunks))}/{len(chunks)}")

    def similarity_search(self, query, k=5):
        return self.db.similarity_search(query=query, k=k)

    def similarity_search_with_score(self, query, k=5):
        return self.db.similarity_search_with_score(query=query, k=k)
    
    def get_len(self):
        return self.db._collection.count()

    def as_retriever(self, **kwargs):
        return self.db.as_retriever(**kwargs)
    
    def get_documents(self):
        return self.db._collection.get()
    
    def get_by_symbol(self, symbol: str) -> list[Document]:

        results = self.db._collection.get(
            where={
                "symbol": symbol
            }
        )
        if not results["documents"]:
            return []

        if not results["metadatas"]:
            return []

        documents = []
        metadatas = results["metadatas"] or []
        documents_data = results["documents"] or []
        for i in range(len(results["ids"])):

            metadata = metadatas[i]

            documents.append(
                Document(
                    page_content=documents_data[i],
                    metadata=metadata
                )
            )

        return documents


    def get_by_symbols(self, symbols: list[str]) -> list[Document]:

        documents = []
        seen = set()

        for symbol in symbols:

            results = self.get_by_symbol(symbol)

            for doc in results:

                key = (doc.metadata.get("source"),doc.metadata.get("symbol"))

                if key in seen:
                    continue

                seen.add(key)
                documents.append(doc)

        return documents
    def clear(self):
        try:
            self.db.delete_collection()
        except Exception:
            pass

        self.db = Chroma(
            collection_name=self.collection_name,
            embedding_function=self.embedding_model,
            persist_directory="data/chroma_db"
        )