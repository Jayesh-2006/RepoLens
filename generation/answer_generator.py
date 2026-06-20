from models import RetrievedDocument

from .prompts import SYSTEM_PROMPT


class AnswerGenerator:

    def __init__(self, llm):
        self.llm = llm

    def build_context(self, documents: list[RetrievedDocument]) -> str:

        parts = []

        for i, doc in enumerate(documents, start=1):
            parts.append(
                f"[DOCUMENT {i}]\n" 
                f"FILE: {doc.source}\n"
                f"SYMBOL: {doc.symbol}\n"
                f"TYPE: {doc.chunk_type or 'unknown'}\n\n"
                f"{doc.page_content}"
            )

        return "\n\n".join(parts)

    def generate(self,query: str,documents: list[RetrievedDocument]):

        context = self.build_context(documents)

        messages = [
                    {
                        "role": "system",
                        "content": SYSTEM_PROMPT
                    },
                    {
                        "role": "user",
                        "content": (
                            "Use ONLY the context between <context> tags."
                            f"Repository Context:\n\n"
                            "<context>"
                            f"{context}"
                            "</context>"
                            f"Question:\n{query}"
                        )
                    }
                ]

        response = self.llm.invoke(messages)

        return response.content, context