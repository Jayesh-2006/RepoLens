"""
Script to index a code repository into the graph database and vector store.
"""

import os

from graph.neo4j_client import Neo4jClient
from graph.graph_builder import GraphBuilder

from indexing.vectordb import VectorStore
from indexing.index_repository import RepositoryIndexer
from pathlib import Path
import sys
from dotenv import load_dotenv
import time

load_dotenv()


if __name__ == "__main__":

    if len(sys.argv) != 2:
        print("Usage: py -m scripts.index_repo <repo_name>")
        sys.exit(1)

    repo_name = sys.argv[1]
    repo_path = f"data/repos/{repo_name}"

    if not Path(repo_path).exists():
        print(f"Repository not found: {repo_path}")
        sys.exit(1)
    
    st = time.time()

    print("Initializing Graph client...")
    client = Neo4jClient(
        uri=os.getenv("NEO4J_URI"),
        username=os.getenv("NEO4J_USERNAME"),
        password=os.getenv("NEO4J_PASSWORD")
    )

    
    print("Initializing Vector Store...")

    vector_store = VectorStore(
        collection_name= repo_name
    )

    graph_builder = GraphBuilder(client)

    indexer = RepositoryIndexer(
        vector_store=vector_store,
        graph_builder=graph_builder
    )

    stats = indexer.index(
        repo_path,
        reset=True
    )

    print("\nIndexing Complete")
    print(f"Repository: {repo_name}")
    print(stats)
    print(f"Indexing time: {time.time() - st:.2f}s")

    print("\nNext step:")
    print(f"py -m scripts.chat {repo_name}")