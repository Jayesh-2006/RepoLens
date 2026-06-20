from ingest.loader import load_repository

from ingest.chunk_documents import Chunker

from graph.graph_analyzer import GraphAnalyzer
from graph.graph_builder import GraphBuilder

from indexing.vectordb import VectorStore


class RepositoryIndexer:

    def __init__(self,vector_store: VectorStore,graph_builder: GraphBuilder):

        self.vector_store = vector_store
        self.graph_builder = graph_builder

        self.chunker = Chunker()
        self.graph_analyzer = GraphAnalyzer()

    def index(self, repo_path: str, reset: bool = False):

        if reset:
            print("Resetting vector store & graph database...")
            self.vector_store.clear()
            self.graph_builder.client.clear()

        print("Loading repository...")
        documents = load_repository(repo_path)

        # print(f"Loaded {len(documents)} files")

        print("Chunking documents...")
        chunks = self.chunker.chunk_documents(documents)

        # print(f"Generated {len(chunks)} chunks")

        print("Building vector index...")
        self.vector_store.add_documents(chunks)

        print("Analyzing graph entities...")
        entities = self.graph_analyzer.analyze_documents(documents)

        # print(f"Generated {len(entities)} graph entities")

        print("Building graph...")
        self.graph_builder.build(entities)

        print("Indexing complete")

        return {
            "files": len(documents),
            "chunks": len(chunks),
            "entities": len(entities)
        }