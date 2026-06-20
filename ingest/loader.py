"""
loads cloned repo
"""

import os
from langchain_core.documents import Document

SUPPORTED_EXTENSIONS = {".py", ".md", ".txt"}

IGNORE_DIRS = {
    ".git",
    "__pycache__",
    "venv",
    ".venv",
    "node_modules"
}

def load_repository(repo_path: str) -> list[Document]:
    documents = []

    for root, dirs, files in os.walk(repo_path):

        dirs[:] = [d for d in dirs if d not in IGNORE_DIRS]

        for file in files:

            extension = os.path.splitext(file)[1]

            if extension not in SUPPORTED_EXTENSIONS:
                continue

            file_path = os.path.join(root, file)

            try:
                with open(file_path,"r",encoding="utf-8",errors="ignore") as f:
                    relative_path = os.path.relpath(file_path,repo_path)
                    
                    documents.append(Document(
                        page_content=f.read(),
                        metadata={
                            "source": relative_path,
                            "extension": extension,
                            "type": "code" if extension == ".py" else "docs"
                        }
                    ))

            except Exception:
                continue

    return documents