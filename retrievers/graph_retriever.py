from graph.neo4j_client import Neo4jClient
from indexing.vectordb import VectorStore
from models import RetrievedDocument

class GraphRetriever:

    def __init__(self, client: Neo4jClient, vectorStore: VectorStore):
        self.client = client
        self.db = vectorStore

    def retrieve(self, documents: list[RetrievedDocument], hops :int = 1) -> list[str]:

        symbols = set()

        for document in documents:

            symbol = document.symbol

            if symbol:
                symbols.add(symbol)

        expanded_symbols = set()

        for symbol in symbols:

            neighbours = self._get_neighbours(symbol, hops = hops)

            expanded_symbols.update(neighbours)

        return list(expanded_symbols)

    def _get_neighbours(self, symbol: str, hops :int = 1) -> list[str]:

        query = f"""
        MATCH (n {{symbol:$symbol}})-[*1..{hops}]-(m)
        RETURN DISTINCT m.symbol AS symbol
        """

        result = self.client.execute(
            query,
            {"symbol": symbol}
        )

        return [
            record["symbol"]
            for record in result
            if record["symbol"]
        ]