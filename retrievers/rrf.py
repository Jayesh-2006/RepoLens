from models import RetrievedDocument

EXTENSION_WEIGHTS = {
        ".py": 1.2,
        ".md": 1.0,
        ".txt": 0.9
    }

def reciprocal_rank_fusion(rankings, weights, fusion_k=60) ->list[RetrievedDocument]:

    scores = {}

    documents = {}

    for i, ranking in enumerate(rankings):
        weight = weights[i]

        for rank, result in enumerate(ranking):

            key = (result.source,result.chunk_id)

            documents[key] = result

            scores[key] = scores.get(key, 0) + (weight / (fusion_k + rank+1))

    # for key in scores:
    #     doc = documents[key]
    #     scores[key] *= EXTENSION_WEIGHTS.get(doc.extension,1.0)


    ranked = sorted(scores.items(),
        key=lambda x: x[1],
        reverse=True
    )

    fused = []

    for rank, (key, score) in enumerate(ranked):
        doc = documents[key]
        fused.append(
            RetrievedDocument(
                page_content=doc.page_content,
                source=doc.source,
                chunk_id=doc.chunk_id,
                extension=doc.extension,
                retriever="hybrid",
                rank=rank + 1,
                score=score,
                symbol=doc.symbol,
                chunk_type=doc.chunk_type
            )
        )

    return fused