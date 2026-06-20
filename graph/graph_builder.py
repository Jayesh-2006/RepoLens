from langchain_core.documents import Document


from .neo4j_client import Neo4jClient


class GraphBuilder:

    def __init__(self,client: Neo4jClient):
        self.client = client

    def build(self,chunks: list[Document]):
        
        processed_files = set()
        known_symbols = set()

        call_chunks = []

        for chunk in chunks:

            chunk_type = chunk.metadata.get("chunk_type")

            if chunk_type in ["function","method","class"]:
                known_symbols.add(chunk.metadata["symbol"])

        for chunk in chunks:

            source = chunk.metadata["source"]
            
            if source not in processed_files:
                self._create_file_node(source)
                processed_files.add(source)

            chunk_type = chunk.metadata.get("chunk_type")
            
            if chunk_type == "class":

                self._create_class_node(
                    source=source,
                    class_name=chunk.metadata["symbol"]
                )

            elif chunk_type == "function":

                self._create_function_node(
                    source=source,
                    function_name=chunk.metadata["symbol"]
                )

            elif chunk_type == "method":

                class_name = chunk.metadata["parent_class"]

                method_name = chunk.metadata["method_name"]

                self._create_method_node(
                    source=source,
                    class_name=class_name,
                    method_name=method_name
                )
            elif chunk_type == "import":

                self._create_import_relation(
                    source=chunk.metadata["source"],
                    module=chunk.metadata["module"]
                )
            elif chunk_type == "call":
                call_chunks.append(chunk)
                
        for chunk in call_chunks:
            caller = chunk.metadata["caller"]
            callee = chunk.metadata["callee"]
            source = chunk.metadata["source"]
            if callee not in known_symbols:
                continue

            
            self._create_call_relation(
                source=source,
                caller=caller,
                callee=callee
            )
                
        

    def _create_call_relation(self,source: str,caller: str,callee: str):

        
        self.client.execute(
            """
            MATCH (a)
            WHERE (a:Function OR a:Method OR a:Class)
            AND a.symbol = $caller
            AND a.source = $source

            MATCH (b)
            WHERE (b:Function OR b:Method OR b:Class)
            AND b.symbol = $callee

            MERGE (a)-[:CALLS]->(b)
            """,
            {
                "source": source,
                "caller": caller,
                "callee": callee
            }
        )

    def _create_file_node(self,source: str):

        self.client.execute(
            """
            MERGE (f:File {path:$source})
            """,
            {
                "source": source
            }
        )

    def _create_class_node(self,source: str,class_name: str):

        self.client.execute(
            """
            MERGE (f:File {path:$source})

            MERGE (c:Class {
                name:$class_name,
                source:$source,
                symbol:$class_name
            })

            MERGE (f)-[:CONTAINS]->(c)
            """,
            {
                "source": source,
                "class_name": class_name
            }
        )

    def _create_function_node(self,source: str,function_name: str):

        self.client.execute(
            """
            MERGE (f:File {path:$source})

            MERGE (fn:Function {
                name:$function_name,
                source:$source,
                symbol:$function_name
            })

            MERGE (f)-[:CONTAINS]->(fn)
            """,
            {
                "source": source,
                "function_name": function_name
            }
        )

    def _create_method_node(self,source: str,class_name: str,method_name: str):

        self.client.execute(
            """
            MERGE (c:Class {
                name:$class_name,
                source:$source,
                symbol:$class_name
            })

            MERGE (m:Method {
                symbol:$symbol,
                source:$source,
                name:$method_name,
                class_name:$class_name
            })

            MERGE (c)-[:CONTAINS]->(m)
            """,
            {
                "source": source,
                "class_name": class_name,
                "method_name": method_name,
                "symbol": f"{class_name}.{method_name}"
            }
        )
    def _create_import_relation(self,source: str,module: str):

        self.client.execute(
            """
            MERGE (f:File {path:$source})

            MERGE (m:Module {
                name:$module
            })

            MERGE (f)-[:IMPORTS]->(m)
            """,
            {
                "source": source,
                "module": module
            }
        )