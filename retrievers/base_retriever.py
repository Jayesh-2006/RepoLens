"""
abstarct base retriever class
"""


from abc import ABC, abstractmethod

from models import RetrievedDocument

class BaseRetriever(ABC):

    @abstractmethod
    def retrieve(self, query: str, top_k: int = 5) -> list[RetrievedDocument]:
        """
        Retrieve relevant documents based on the query.

        Args:
            query (str): The input query for which relevant documents need to be retrieved.
            top_k (int): The number of top relevant documents to retrieve.

        Returns:
            List[Document]: A list of retrieved documents relevant to the query.
        """
        pass
    