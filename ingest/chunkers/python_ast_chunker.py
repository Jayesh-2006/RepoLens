import ast

from langchain_core.documents import Document

from .base_chunker import BaseChunker

class PythonASTChunker(BaseChunker):

    def __init__(self):
        pass

    def chunk(self, document: Document) -> list[Document]:

        tree = ast.parse(document.page_content)
        
        chunks = []
        

        for node in ast.iter_child_nodes(tree):

            if  isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):

                metadata = document.metadata.copy()
                metadata["symbol"] = node.name
                metadata["chunk_type"] = "function"

                chunks.append(
                    Document(page_content=str(ast.get_source_segment(document.page_content,node)),metadata=metadata)
                )
                
            elif isinstance(node, ast.ClassDef):

                methods = [child.name 
                           for child in node.body 
                           if isinstance(child, (ast.FunctionDef,ast.AsyncFunctionDef))
                        ]
                metadata = document.metadata.copy()
                metadata["symbol"] = node.name
                metadata["chunk_type"] = "class"

                class_content = (
                    f"class {node.name}\n\n"
                    f"Methods:\n" +
                    "\n".join(f"- {method}" for method in methods)
                )

                chunks.append(Document(page_content=class_content, metadata=metadata))

                for child in node.body:

                    if not isinstance(child,(ast.FunctionDef,ast.AsyncFunctionDef)):
                        continue

                    metadata = document.metadata.copy()

                    metadata["chunk_type"] = "method"
                    metadata["method_name"] = child.name
                    metadata["symbol"] = (
                        f"{node.name}.{child.name}"
                    )

                    metadata["parent_class"] = node.name

                    method_source = ast.get_source_segment(document.page_content,child)
                    page_content = (
                        f"File: {document.metadata['source']}\n"
                        f"Class: {node.name}\n"
                        f"Method: {child.name}\n\n"
                        f"{method_source}"
                    )

                    chunks.append(
                        Document(page_content= page_content,metadata=metadata)
                    )
            elif isinstance(node, ast.Assign):

                targets = [target.id for target in node.targets if isinstance(target, ast.Name)]

                for target in targets:
                    metadata = document.metadata.copy()
                    metadata["symbol"] = target
                    metadata["chunk_type"] = "variable"

                    variable_source = ast.get_source_segment(document.page_content,node)
                    page_content = (
                        f"File: {document.metadata['source']}\n"
                        f"Type: Variable\n"
                        f"Variable: {target}\n\n"
                        f"{variable_source}"
                    )

                    chunks.append(
                        Document(page_content=page_content,metadata=metadata)
                    )

            elif isinstance(node, ast.AnnAssign):

                if isinstance(node.target, ast.Name):

                    metadata = document.metadata.copy()

                    metadata["symbol"] = node.target.id
                    metadata["chunk_type"] = "variable"

                    variable_source = ast.get_source_segment(document.page_content,node)

                    page_content = (
                        f"File: {document.metadata['source']}\n"
                        f"Type: Variable\n"
                        f"Variable: {node.target.id}\n\n"
                        f"{variable_source}"
                    )

                    chunks.append(
                        Document(
                            page_content=page_content,
                            metadata=metadata
                        )
                    )

        return chunks