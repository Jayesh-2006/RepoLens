
from sentence_transformers import CrossEncoder

from models import RetrievedDocument


class CrossEncoderReranker:

    def __init__(self,model_name="cross-encoder/ms-marco-MiniLM-L-6-v2", device : str = "cpu"):
        self.model = CrossEncoder(model_name, device = device)

    def rerank(self,query: str,documents: list[RetrievedDocument],top_k: int = 5) -> list[RetrievedDocument]:

        if not documents:
            return []

        pairs = [(query, doc.page_content[:2000]) for doc in documents]

        scores = self.model.predict(pairs, batch_size=8)

        ranked = sorted(
            zip(documents, scores),
            key=lambda x: x[1],
            reverse=True
        )

        results = []

        for rank, (doc, score) in enumerate(ranked[:top_k]):

            doc.score = float(score)
            doc.rank = rank + 1

            results.append(doc)

        return results