from langchain_core.documents import Document
from .chunker_factory import get_chunker



class Chunker:

    def __init__(self):
        pass

    def chunk_documents(self,documents: list[Document]) -> list[Document]:

        chunks = []
        global_chunk_id = 0

        for document in documents:
            extension = str(document.metadata.get("extension"))
            chunker = get_chunker(extension)

            chunked_docs = chunker.chunk(document)
            
            for chunk in chunked_docs:

                chunk.metadata["chunk_id"] = global_chunk_id
                global_chunk_id += 1

            
            chunks.extend(chunked_docs)
            

        return chunks