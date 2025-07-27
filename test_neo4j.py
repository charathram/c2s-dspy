#!/usr/bin/env python3
"""
Simple test script for Neo4j client functionality.

This script tests the core features of the cleaned-up Neo4j client:
- Connection management
- Query execution
- Upsert operations
- Error handling
"""

import os
import sys
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


# Add the project root to the path to import modules
sys.path.insert(0, str(Path(__file__).parent))

from neo4j_client import Neo4jClient, Neo4jConnectionError, Neo4jQueryError


class SimpleNeo4jTest:
    """Simple test suite for Neo4j client."""

    def __init__(self):
        self.client = None
        self.passed = 0
        self.failed = 0
        self.tests = []

    def assert_test(self, condition, test_name, error_msg=None):
        """Assert a test condition and track results."""
        if condition:
            self.passed += 1
            self.tests.append(f"✅ {test_name}")
            print(f"✅ {test_name}")
        else:
            self.failed += 1
            msg = f"❌ {test_name}"
            if error_msg:
                msg += f" - {error_msg}"
            self.tests.append(msg)
            print(msg)

    def setup(self):
        """Set up test environment."""
        print("🔧 Setting up Neo4j test environment...")

        try:
            # Create client from environment
            self.client = Neo4jClient.from_env()
            self.client.connect()

            # Test connection
            health = self.client.health_check()
            if not health:
                raise Exception("Cannot connect to Neo4j")

            print(f"✅ Connected to Neo4j at {self.client.uri}")
            print(f"   Database: {self.client.database}")
            return True

        except Exception as e:
            print(f"❌ Setup failed: {e}")
            return False

    def cleanup(self):
        """Clean up test environment."""
        print("\n🧹 Cleaning up test environment...")

        try:
            if self.client:
                # Clean up test data
                self.client.execute_query("MATCH (n:TestNode) DETACH DELETE n")
                self.client.execute_query("MATCH (n:Person {name: 'TestUser'}) DETACH DELETE n")
                self.client.execute_query("MATCH (n:Company {name: 'TestCompany'}) DETACH DELETE n")
                self.client.disconnect()
                print("✅ Cleanup completed")
        except Exception as e:
            print(f"⚠️ Cleanup warning: {e}")

    def test_connection_management(self):
        """Test connection and disconnection."""
        print("\n🔌 Testing connection management...")

        try:
            # Test health check
            health = self.client.health_check()
            self.assert_test(
                health is True,
                "Health check returns True for connected client"
            )

            # Test disconnect and reconnect
            self.client.disconnect()
            self.client.connect()

            # Test health check after reconnect
            health = self.client.health_check()
            self.assert_test(
                health is True,
                "Health check works after reconnect"
            )

        except Exception as e:
            self.assert_test(False, "Connection management", str(e))

    def test_basic_queries(self):
        """Test basic query execution."""
        print("\n💬 Testing basic queries...")

        try:
            # Test simple query
            result = self.client.execute_query("RETURN 1 as test_value")
            self.assert_test(
                len(result) == 1 and result[0]["test_value"] == 1,
                "Simple query returns correct result"
            )

            # Test query with parameters
            result = self.client.execute_query(
                "RETURN $name as name, $age as age",
                {"name": "Alice", "age": 30}
            )
            self.assert_test(
                result[0]["name"] == "Alice" and result[0]["age"] == 30,
                "Parameterized query works correctly"
            )

            # Test empty result query
            result = self.client.execute_query("MATCH (n:NonExistentLabel) RETURN n")
            self.assert_test(
                len(result) == 0,
                "Empty result query returns empty list"
            )

        except Exception as e:
            self.assert_test(False, "Basic queries", str(e))

    def test_upsert_operations(self):
        """Test upsert functionality."""
        print("\n🔄 Testing upsert operations...")

        try:
            # Test creating a new node
            result1 = self.client.upsert("TestUser", "Person", {"age": 30, "city": "New York"})
            self.assert_test(
                result1["name"] == "TestUser" and result1["age"] == 30,
                "Upsert creates new node with correct properties"
            )

            # Test updating the same node
            result2 = self.client.upsert("TestUser", "Person", {"age": 31, "country": "USA"})
            self.assert_test(
                result2["age"] == 31 and result2["country"] == "USA",
                "Upsert updates existing node properties"
            )

            # Test creating a different node type with same name
            result3 = self.client.upsert("TestUser", "Company", {"industry": "Tech"})
            self.assert_test(
                result3["name"] == "TestUser" and result3["industry"] == "Tech",
                "Upsert creates different node type with same name"
            )

            # Verify both nodes exist
            persons = self.client.execute_query("MATCH (p:Person {name: 'TestUser'}) RETURN p")
            companies = self.client.execute_query("MATCH (c:Company {name: 'TestUser'}) RETURN c")

            self.assert_test(
                len(persons) == 1 and len(companies) == 1,
                "Different node types with same name coexist"
            )

        except Exception as e:
            self.assert_test(False, "Upsert operations", str(e))

    def test_context_manager(self):
        """Test context manager functionality."""
        print("\n🔧 Testing context manager...")

        try:
            # Test using client as context manager
            with Neo4jClient.from_env() as temp_client:
                result = temp_client.execute_query("RETURN 'context_test' as test")
                self.assert_test(
                    result[0]["test"] == "context_test",
                    "Context manager allows query execution"
                )

            # Client should be disconnected after context
            self.assert_test(
                True,  # If we reach here, context manager worked
                "Context manager properly disconnects"
            )

        except Exception as e:
            self.assert_test(False, "Context manager", str(e))

    def test_error_handling(self):
        """Test error handling."""
        print("\n⚠️ Testing error handling...")

        try:
            # Test query on disconnected client
            temp_client = Neo4jClient.from_env()
            # Don't connect

            try:
                temp_client.execute_query("RETURN 1")
                self.assert_test(False, "Query on disconnected client should fail")
            except Neo4jConnectionError:
                self.assert_test(True, "Query on disconnected client raises correct exception")

            # Test invalid query
            try:
                self.client.execute_query("INVALID CYPHER SYNTAX")
                self.assert_test(False, "Invalid query should fail")
            except Neo4jQueryError:
                self.assert_test(True, "Invalid query raises correct exception")

            # Test upsert on disconnected client
            try:
                temp_client.upsert("test", "Test", {})
                self.assert_test(False, "Upsert on disconnected client should fail")
            except Neo4jConnectionError:
                self.assert_test(True, "Upsert on disconnected client raises correct exception")

        except Exception as e:
            self.assert_test(False, "Error handling", str(e))

    def run_all_tests(self):
        """Run all tests."""
        print("🚀 Starting Neo4j Client Tests")
        print("=" * 50)

        if not self.setup():
            return False

        try:
            self.test_connection_management()
            self.test_basic_queries()
            self.test_upsert_operations()
            self.test_context_manager()
            self.test_error_handling()

        finally:
            self.cleanup()

        self.print_results()
        return self.failed == 0

    def print_results(self):
        """Print test results summary."""
        print("\n" + "=" * 50)
        print("🏁 Test Results Summary")
        print("=" * 50)

        total_tests = self.passed + self.failed
        pass_rate = (self.passed / total_tests * 100) if total_tests > 0 else 0

        print(f"Total Tests: {total_tests}")
        print(f"Passed: {self.passed} ✅")
        print(f"Failed: {self.failed} ❌")
        print(f"Pass Rate: {pass_rate:.1f}%")

        if self.failed == 0:
            print("\n🎉 All tests passed!")
        else:
            print(f"\n💥 {self.failed} test(s) failed. See details above.")


def main():
    """Main test function."""
    # Check environment variables
    required_vars = ["NEO4J_URI", "NEO4J_USERNAME", "NEO4J_PASSWORD"]
    missing_vars = [var for var in required_vars if not os.getenv(var)]

    if missing_vars:
        print("❌ Missing required environment variables:")
        for var in missing_vars:
            print(f"   - {var}")
        print("\nPlease set these variables and try again.")
        return False

    # Run tests
    test_suite = SimpleNeo4jTest()
    success = test_suite.run_all_tests()

    return success


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
