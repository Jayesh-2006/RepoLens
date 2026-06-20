"""
Chat interface for querying repositories indexed by RepoLens.
"""

from dotenv import load_dotenv
from langchain_groq import ChatGroq

from graph.neo4j_client import Neo4jClient

from indexing.vectordb import VectorStore

from retrievers.dense_retriever import DenseRetriever
from retrievers.bm25_retriever import BM25Retriever
from retrievers.hybrid_retriever import HybridRetriever
from retrievers.graph_retriever import GraphRetriever
from retrievers.reranker import CrossEncoderReranker

from generation.answer_generator import AnswerGenerator

from repolens import RepoLens
import os
import sys
import time

load_dotenv()


def build_repolens(repo_name: str) -> RepoLens:

    vector_store = VectorStore(collection_name=repo_name,device="cpu")

    dense = DenseRetriever(vector_store)

    bm25 = BM25Retriever(vector_store)

    hybrid = HybridRetriever(
        retrievers=[dense, bm25],
        weights=[1, 1]
    )

    client = Neo4jClient(
        uri=os.getenv("NEO4J_URI"),
        username=os.getenv("NEO4J_USERNAME"),
        password=os.getenv("NEO4J_PASSWORD")
    )

    graph_retriever = GraphRetriever(
        client,
        vector_store
    )

    reranker = CrossEncoderReranker(
        "BAAI/bge-reranker-v2-m3",
        device="cuda"
    )

    llm = ChatGroq(
        model="llama-3.3-70b-versatile",
        temperature=0
    )

    generator = AnswerGenerator(llm)

    return RepoLens(
        retriever=hybrid,
        reranker=reranker,
        generator=generator,
        graph_retriever=graph_retriever
    )


def main():
    if len(sys.argv) != 2:
        print("Usage: py -m scripts.chat <repo_name>")
        sys.exit(1)

    repo_name = sys.argv[1]

    repo_path = f"data/repos/{repo_name}"

    if not os.path.exists(repo_path):
        print(f"Repository not found: {repo_path}")
        print("\nClone and index the repository first.")
        print(f"py -m scripts.clone_repo <repo_url> {repo_name}")
        print(f"py -m scripts.index_repo {repo_name}")
        sys.exit(1)
    
    repolens = build_repolens(repo_name)

    print("RepoLens Ready")
    print("Type 'exit' to quit\n")

    while True:

        query = input("Query: ").strip()

        if query.lower() == "exit":
            break

        start = time.time()

        answer, _, _, _ = repolens.ask(query)

        print("\n" + "=" * 80)
        print(answer)
        print("=" * 80)

        print(f"\nCompleted in {time.time() - start:.2f}s\n")


if __name__ == "__main__":
    main()