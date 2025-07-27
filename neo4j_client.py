import logging
from typing import Optional, Any, Dict, List
from neo4j import GraphDatabase, Driver
from neo4j.exceptions import ServiceUnavailable, AuthError
import os
from dotenv import load_dotenv


class Neo4jConnectionError(Exception):
    """Raised when Neo4j connection fails"""
    pass


class Neo4jQueryError(Exception):
    """Raised when Neo4j query execution fails"""
    pass


class Neo4jClient:
    """
    Simple Neo4j client for basic database operations.
    Provides connection management and query execution.
    """

    def __init__(self, uri: str, username: str, password: str, database: str = "neo4j"):
        """
        Initialize Neo4j client.

        Args:
            uri: Neo4j database URI (e.g., "bolt://localhost:7687")
            username: Database username
            password: Database password
            database: Database name (default: "neo4j")
        """
        self.uri = uri
        self.username = username
        self.password = password
        self.database = database
        self.driver: Optional[Driver] = None
        self.logger = logging.getLogger(__name__)

    def connect(self) -> None:
        """
        Establish connection to Neo4j database.

        Raises:
            Neo4jConnectionError: If connection fails
        """
        try:
            self.driver = GraphDatabase.driver(
                self.uri,
                auth=(self.username, self.password)
            )
            # Test the connection
            with self.driver.session(database=self.database) as session:
                session.run("RETURN 1")
            self.logger.info(f"Connected to Neo4j at {self.uri}")
        except (ServiceUnavailable, AuthError) as e:
            raise Neo4jConnectionError(f"Failed to connect to Neo4j: {e}")

    def disconnect(self) -> None:
        """Close the Neo4j connection."""
        if self.driver:
            self.driver.close()
            self.driver = None
            self.logger.info("Disconnected from Neo4j")

    def __enter__(self):
        """Context manager entry."""
        self.connect()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit."""
        self.disconnect()

    def _ensure_connected(self) -> None:
        """Ensure the client is connected to the database."""
        if not self.driver:
            raise Neo4jConnectionError("Not connected to Neo4j. Call connect() first.")

    def execute_query(self, query: str, parameters: Optional[Dict[str, Any]] = None) -> List[Dict[str, Any]]:
        """
        Execute a Cypher query and return results.

        Args:
            query: Cypher query string
            parameters: Query parameters (optional)

        Returns:
            List of result records as dictionaries

        Raises:
            Neo4jConnectionError: If not connected
            Neo4jQueryError: If query execution fails
        """
        self._ensure_connected()

        try:
            with self.driver.session(database=self.database) as session:
                result = session.run(query, parameters or {})
                records = []
                for record in result:
                    records.append(dict(record))
                return records
        except Exception as e:
            self.logger.error(f"Query execution failed: {e}")
            raise Neo4jQueryError(f"Failed to execute query: {e}")

    def upsert(self, node_name: str, node_type: str, properties: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Create or update a node with the specified name and type.

        Args:
            node_name: Name of the node (will be stored as 'name' property)
            node_type: Type/label of the node
            properties: Additional properties for the node (optional)

        Returns:
            Dictionary containing the created/updated node data

        Raises:
            Neo4jConnectionError: If not connected
            Neo4jQueryError: If upsert operation fails
        """
        self._ensure_connected()

        if properties is None:
            properties = {}

        # Ensure name is included in properties
        properties['name'] = node_name

        # Build the query dynamically to handle the node type
        query = f"""
        MERGE (n:{node_type} {{name: $name}})
        SET n += $properties
        RETURN n
        """

        try:
            result = self.execute_query(query, {
                'name': node_name,
                'properties': properties
            })

            if result:
                node_data = dict(result[0]['n'])
                self.logger.debug(f"Upserted {node_type} node: {node_name}")
                return node_data
            else:
                raise Neo4jQueryError("No result returned from upsert operation")

        except Exception as e:
            self.logger.error(f"Failed to upsert node {node_name} of type {node_type}: {e}")
            raise Neo4jQueryError(f"Failed to upsert node: {e}")

    @classmethod
    def from_env(cls) -> 'Neo4jClient':
        """
        Create Neo4j client from environment variables.
        Expected variables: NEO4J_URI, NEO4J_USERNAME, NEO4J_PASSWORD, NEO4J_DATABASE

        Returns:
            Neo4jClient instance
        """
        import os

        uri = os.getenv("NEO4J_URI", "bolt://localhost:7687")
        username = os.getenv("NEO4J_USERNAME", "neo4j")
        password = os.getenv("NEO4J_PASSWORD")
        database = os.getenv("NEO4J_DATABASE", "neo4j")

        if not password:
            raise ValueError("NEO4J_PASSWORD environment variable is required")

        return cls(uri, username, password, database)

    def health_check(self) -> bool:
        """
        Check if the Neo4j connection is healthy.

        Returns:
            True if connection is healthy, False otherwise
        """
        try:
            self._ensure_connected()
            with self.driver.session(database=self.database) as session:
                session.run("RETURN 1")
            return True
        except Exception as e:
            self.logger.error(f"Health check failed: {e}")
            return False

def main():
    load_dotenv()

    with Neo4jClient.from_env() as client:
        if client.health_check():
            print("Neo4j connection is healthy")
        else:
            print("Neo4j connection is not healthy")
        client.upsert("Test", "`TST LBL`", {"file": "example.txt", "size": 1024, "type": "text/plain"})
        client.upsert("Test2", "TST_LBL", {"file": "example2.txt", "size": 2048, "type": "text/plain"})
        client.upsert("Test3", "TST_LBL", {"file": "example3.txt", "size": 3072, "type": "text/plain"})

if __name__ == "__main__":
    main()
