from retrievers.rrf import reciprocal_rank_fusion
from models import RetrievedDocument

class HybridRetriever:

    def __init__(self,retrievers: list, weights: list):
        if len(retrievers) != len(weights):
            raise ValueError("retrievers and weights must have same length")
        self.retrievers = retrievers
        self.weights = weights

    def retrieve(self,query: str,retrieval_k: int = 20,top_k: int = 5,fusion_k: int = 10) -> list[RetrievedDocument]:
        
        results = []
        for retriever in self.retrievers:
            results.append(retriever.retrieve(query, top_k=retrieval_k))

        fused = reciprocal_rank_fusion(results, self.weights, fusion_k=fusion_k)

        return fused[:top_k]
    