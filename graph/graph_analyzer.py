import ast

from langchain_core.documents import Document



class GraphAnalyzer():

    def analyze(self, document: Document) -> list[Document]:

        tree = ast.parse(document.page_content)
        
        entities = []
        
        
        for node in ast.iter_child_nodes(tree):

            if  isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):

                metadata = document.metadata.copy()
                metadata["symbol"] = node.name
                metadata["chunk_type"] = "function"

                entities.append(
                    Document(page_content=str(ast.get_source_segment(document.page_content,node)),metadata=metadata)
                )
                for child in ast.walk(node):
                        

                        if not isinstance(child,ast.Call):
                            continue

                        if isinstance(child.func,ast.Name):

                            if node.name == child.func.id:
                                continue

                            metadata = document.metadata.copy()

                            metadata["chunk_type"] = "call"
                            metadata["caller"] = node.name
                            metadata["callee"] = child.func.id

                            entities.append(
                                Document(
                                    page_content="",
                                    metadata=metadata
                                )
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

                entities.append(Document(page_content=class_content, metadata=metadata))

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

                    entities.append(
                        Document(page_content= page_content,metadata=metadata)
                    )
                    for call in ast.walk(child):

                        if not isinstance(call,ast.Call):
                            continue

                        if isinstance(call.func,ast.Name):

                            if child.name == call.func.id:
                                continue

                            metadata = document.metadata.copy()

                            metadata["chunk_type"] = "call"
                            metadata["caller"] = f"{node.name}.{child.name}"
                            metadata["callee"] = call.func.id

                            entities.append(
                                Document(
                                    page_content="",
                                    metadata=metadata
                                )
                            )

                        elif isinstance(call.func,ast.Attribute):

                            if not isinstance(call.func.value,ast.Name):
                                continue

                            if call.func.value.id != "self":
                                continue

                            if child.name == call.func.attr:
                                continue

                            metadata = document.metadata.copy()

                            metadata["chunk_type"] = "call"
                            metadata["caller"] = f"{node.name}.{child.name}"
                            metadata["callee"] = f"{node.name}.{call.func.attr}"

                            entities.append(
                                Document(
                                    page_content="",
                                    metadata=metadata
                                )
                            )
                    
            # elif isinstance(node, ast.Assign):

            #     targets = [target.id for target in node.targets if isinstance(target, ast.Name)]

            #     for target in targets:
            #         metadata = document.metadata.copy()
            #         metadata["symbol"] = target
            #         metadata["chunk_type"] = "variable"

            #         variable_source = ast.get_source_segment(document.page_content,node)
            #         page_content = (
            #             f"File: {document.metadata['source']}\n"
            #             f"Type: Variable\n"
            #             f"Variable: {target}\n\n"
            #             f"{variable_source}"
            #         )

            #         entities.append(
            #             Document(page_content=page_content,metadata=metadata)
            #         )

            # elif isinstance(node, ast.AnnAssign):

            #     if isinstance(node.target, ast.Name):

            #         metadata = document.metadata.copy()

            #         metadata["symbol"] = node.target.id
            #         metadata["chunk_type"] = "variable"

            #         variable_source = ast.get_source_segment(document.page_content,node)

            #         page_content = (
            #             f"File: {document.metadata['source']}\n"
            #             f"Type: Variable\n"
            #             f"Variable: {node.target.id}\n\n"
            #             f"{variable_source}"
            #         )

            #         entities.append(
            #             Document(
            #                 page_content=page_content,
            #                 metadata=metadata
            #             )
            #         )
            elif isinstance(node, ast.Import):

                for alias in node.names:

                    metadata = document.metadata.copy()

                    metadata["chunk_type"] = "import"
                    metadata["module"] = alias.name

                    page_content = (
                        f"File: {document.metadata['source']}\n"
                        f"Type: Import\n"
                        f"Module: {alias.name}"
                    )

                    entities.append(
                        Document(
                            page_content=page_content,
                            metadata=metadata
                        )
                    )
            elif isinstance(node, ast.ImportFrom):

                module = node.module or ""

                for alias in node.names:

                    metadata = document.metadata.copy()

                    
                    metadata["chunk_type"] = "import"
                    
                    metadata["module"] = module
                    metadata["imported"] = alias.name

                    page_content = (
                        f"File: {document.metadata['source']}\n"
                        f"Type: Import\n"
                        f"Module: {module}\n"
                        f"Imported: {alias.name}"
                    )

                    entities.append(
                        Document(
                            page_content=page_content,
                            metadata=metadata
                        )
                    )

        return entities
    
    def analyze_documents(self, documents: list[Document]) -> list[Document]:

        all_entities = []

        for document in documents:
            if document.metadata.get("extension") != ".py":
                continue
            entities = self.analyze(document)
            all_entities.extend(entities)

        return all_entities