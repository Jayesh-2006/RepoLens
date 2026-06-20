from neo4j import GraphDatabase


class Neo4jClient:

    def __init__(self, uri, username, password):
        self.driver = GraphDatabase.driver(
            uri,
            auth=(username, password)
        )

    def execute(self, query , parameters=None):

        with self.driver.session() as session:
            return list(
                session.run(
                    query,
                    parameters or {}
                )
            )

    def close(self):
        self.driver.close()
        
    def clear(self):

        self.execute(
            """
            MATCH (n)
            DETACH DELETE n
            """
        )