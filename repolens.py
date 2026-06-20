from models import RetrievedDocument
from retrievers.graph_retriever import GraphRetriever
from retrievers.hybrid_retriever import HybridRetriever
from retrievers.reranker import CrossEncoderReranker
from generation.answer_generator import AnswerGenerator
# import time

class RepoLens:

    def __init__(self,retriever: HybridRetriever,reranker: CrossEncoderReranker,generator: AnswerGenerator,graph_retriever:GraphRetriever):
        self.retriever = retriever
        self.reranker = reranker
        self.generator = generator
        self.graph_retriever = graph_retriever

    def ask(self,query: str):

        # st = time.time()
        # print("Step 1: Retrieving relevant documents...")
        retrieved = self.retriever.retrieve(query,retrieval_k=30, top_k=20, fusion_k=10)
        # print("Retrieved:", len(retrieved))
        # print(f"Retrieval took {time.time() - st:.2f} seconds")
        
        # st = time.time()
        # print("Step 2: Reranking documents...")
        # print("Reranking", len(retrieved), "documents")
        reranked = self.reranker.rerank(query,retrieved,top_k=10)
        # print(f"Reranking took {time.time() - st:.2f} seconds")
        
        # st = time.time()
        # print("Step 3: Retrieving graph information...")
        graph_res = self.graph_retriever.retrieve(reranked,hops = 2)
        # print("Graph symbols:", len(graph_res))
        # print(f"Graph retrieval took {time.time() - st:.2f} seconds")

        # print("Step 4: Loading graph documents...")
        graph_docs = self.graph_retriever.db.get_by_symbols(graph_res)
        graph_docs = [RetrievedDocument.from_document(doc) for doc in graph_docs]
        # # graph_docs = graph_docs[:5]  # Limit to top 5 graph documents
        seen = set()
        candidate_docs = []

        for doc in reranked + graph_docs:
            key = (doc.source,doc.symbol,doc.chunk_id)

            if key not in seen:
                seen.add(key)
                candidate_docs.append(doc)

        
        # st = time.time()
        # print("Step 5: Final reranking...")
        
        # print("Graph docs:", len(graph_docs))
        # print("All docs:", len(candidate_docs))
        reranked2 = self.reranker.rerank(query,candidate_docs,top_k=8)
        # print(f"Final reranking took {time.time() - st:.2f} seconds")

        # st = time.time()
        # print("Step 6: Generating answer...")
        answer,context = self.generator.generate(query,reranked2)
        # print(f"Answer generation took {time.time() - st:.2f} seconds")

        # print("\nFINAL DOCS")

        # for i, doc in enumerate(reranked2[:5], start=1):
        #     print(
        #         f"{i}. "
        #         f"{doc.source} | "
        #         f"{doc.symbol} | "
        #         f"{doc.chunk_type} | "
        #         f"{doc.score:.4f}"
        #     )
        

        return answer, reranked,reranked2,context
        