# Neo4j Database Setup and Management

This document provides comprehensive instructions for setting up and managing the Neo4j graph database for the C2S-DSPy project.

## Table of Contents

- [Overview](#overview)
- [Quick Start](#quick-start)
- [Installation](#installation)
- [Configuration](#configuration)
- [Management Commands](#management-commands)
- [Connection Information](#connection-information)
- [Backup and Restore](#backup-and-restore)
- [Troubleshooting](#troubleshooting)
- [Advanced Usage](#advanced-usage)

## Overview

Neo4j is a graph database that's perfect for storing and querying code analysis results, dependency relationships, and data model connections. This setup includes:

- Neo4j 5.15 Community Edition
- APOC procedures for advanced graph operations
- Persistent data storage
- Automated backup/restore functionality
- Easy management via Makefile commands

## Quick Start

1. **Start Neo4j**:
   ```bash
   make start
   ```

2. **Open the web interface**:
   ```bash
   make web
   # Or manually visit: http://localhost:7474
   ```

3. **Login credentials**:
   - Username: `neo4j`
   - Password: `password123`

4. **Check status**:
   ```bash
   make status
   ```

## Installation

### Prerequisites

- Docker and Docker Compose installed
- Make utility (available on most Unix-like systems)

### Setup

1. **Clone the repository** (if you haven't already):
   ```bash
   git clone <repository-url>
   cd c2s-dspy
   ```

2. **Start Neo4j**:
   ```bash
   make start
   ```

3. **Verify installation**:
   ```bash
   make status
   ```

The first startup may take 30-60 seconds as Neo4j initializes.

## Configuration

### Environment Variables

The Neo4j configuration is defined in `docker-compose.yml`:

```yaml
environment:
  NEO4J_AUTH: neo4j/password123
  NEO4J_dbms_memory_heap_initial__size: 512m
  NEO4J_dbms_memory_heap_max__size: 2G
  NEO4J_dbms_memory_pagecache_size: 1G
  NEO4J_PLUGINS: '["apoc"]'
```

### Memory Settings

- **Initial Heap**: 512MB
- **Maximum Heap**: 2GB
- **Page Cache**: 1GB

Adjust these settings in `docker-compose.yml` based on your system resources.

### Ports

- **7474**: HTTP web interface
- **7687**: Bolt protocol for database connections

## Management Commands

All Neo4j operations are managed through the Makefile:

### Basic Operations

| Command | Description |
|---------|-------------|
| `make start` | Start Neo4j database |
| `make stop` | Stop Neo4j database |
| `make restart` | Restart Neo4j database |
| `make status` | Show Neo4j status and health |
| `make logs` | View Neo4j logs (follow mode) |
| `make shell` | Open Neo4j Cypher shell |

### Data Management

| Command | Description |
|---------|-------------|
| `make backup` | Create a timestamped backup |
| `make list-backups` | List available backup files |
| `make restore BACKUP_FILE=filename` | Restore from specific backup |
| `make reset` | Delete all data (with confirmation) |

### Maintenance

| Command | Description |
|---------|-------------|
| `make clean` | Clean up Docker resources |
| `make update` | Pull latest Neo4j image |
| `make info` | Show connection information |
| `make web` | Open web interface in browser |
| `make help` | Show all available commands |

## Connection Information

### Web Interface
- **URL**: http://localhost:7474
- **Username**: `neo4j`
- **Password**: `password123`

### Programmatic Access
- **Bolt URL**: `bolt://localhost:7687`
- **Username**: `neo4j`
- **Password**: `password123`

### Python Connection Example

```python
from neo4j import GraphDatabase

class Neo4jConnection:
    def __init__(self, uri, user, password):
        self.driver = GraphDatabase.driver(uri, auth=(user, password))

    def close(self):
        self.driver.close()

    def query(self, query, parameters=None):
        with self.driver.session() as session:
            result = session.run(query, parameters)
            return [record for record in result]

# Usage
conn = Neo4jConnection("bolt://localhost:7687", "neo4j", "password123")
result = conn.query("MATCH (n) RETURN count(n) as node_count")
print(result)
conn.close()
```

To run this example:
```bash
uv run your_neo4j_script.py
```

## Backup and Restore

### Creating Backups

Backups are automatically timestamped and stored in the `./backups` directory:

```bash
make backup
# Creates: backups/neo4j_backup_20231201_143022.dump
```

### Listing Backups

```bash
make list-backups
```

### Restoring from Backup

```bash
make restore BACKUP_FILE=neo4j_backup_20231201_143022.dump
```

**Warning**: Restore operations will replace ALL existing data.

### Backup Schedule

For production use, consider setting up automated backups:

```bash
# Example cron job (daily at 2 AM)
0 2 * * * cd /path/to/c2s-dspy && make backup
```

## Troubleshooting

### Common Issues

#### 1. Container Won't Start

**Symptoms**: `make start` fails or container exits immediately

**Solutions**:
- Check Docker is running: `docker info`
- Check available disk space
- Review logs: `make logs`
- Try cleaning up: `make clean`

#### 2. Web Interface Not Accessible

**Symptoms**: Can't connect to http://localhost:7474

**Solutions**:
- Wait 30-60 seconds for startup
- Check container status: `make status`
- Check if port 7474 is available: `netstat -an | grep 7474`
- Review logs: `make logs`

#### 3. Memory Issues

**Symptoms**: Container crashes or performs poorly

**Solutions**:
- Reduce memory settings in `docker-compose.yml`
- Ensure sufficient system RAM (minimum 4GB recommended)
- Check system resources: `docker stats`

#### 4. Permission Errors

**Symptoms**: Volume mount errors or data persistence issues

**Solutions**:
- Check Docker volume permissions
- Reset volumes: `make reset`
- Ensure Docker has access to the project directory

### Log Analysis

View real-time logs to diagnose issues:

```bash
make logs
```

Common log patterns:
- `Started` - Neo4j has started successfully
- `Remote interface available` - Web interface is ready
- `Bolt enabled` - Database connections are available

### Getting Help

1. **Check logs**: `make logs`
2. **Verify status**: `make status`
3. **Test connectivity**: `curl http://localhost:7474`
4. **Reset if needed**: `make reset`

## Advanced Usage

### APOC Procedures

Neo4j includes APOC (Awesome Procedures on Cypher) for advanced operations:

```cypher
// Import JSON data
CALL apoc.load.json('file:///data.json') YIELD value
CREATE (n:Node {data: value})

// Export data
CALL apoc.export.json.all('export.json', {})

// Graph algorithms
CALL apoc.path.findMany(startNode, endNode, 'RELATIONSHIP', 5)
```

### Custom Configurations

Modify `docker-compose.yml` to add custom configurations:

```yaml
environment:
  # Custom database settings
  NEO4J_dbms_transaction_timeout: 60s
  NEO4J_dbms_query_cache_size: 25
  
  # Security settings
  NEO4J_dbms_security_procedures_whitelist: apoc.*
```

### Multiple Databases

Neo4j supports multiple databases (Enterprise feature simulation in Community):

```cypher
// Create a new database context
CREATE DATABASE codeanalysis;
USE codeanalysis;
```

### Performance Tuning

For large datasets, consider these optimizations:

1. **Index Creation**:
   ```cypher
   CREATE INDEX FOR (n:CodeFile) ON (n.filename)
   CREATE INDEX FOR (n:DataModel) ON (n.name)
   ```

2. **Memory Allocation**:
   ```yaml
   # In docker-compose.yml
   NEO4J_dbms_memory_heap_max__size: 4G
   NEO4J_dbms_memory_pagecache_size: 2G
   ```

3. **Query Optimization**:
   ```cypher
   // Use EXPLAIN to analyze query performance
   EXPLAIN MATCH (n:CodeFile)-[:CONTAINS]->(m:DataModel) RETURN n, m
   ```

### Monitoring

Monitor Neo4j performance through:

- **Web interface**: Metrics and query performance
- **Docker stats**: `docker stats c2s-neo4j`
- **System queries**:
  ```cypher
  CALL dbms.listQueries() YIELD query, elapsedTimeMillis
  CALL dbms.queryJmx('org.neo4j:*') YIELD attributes
  ```

## Integration with C2S-DSPy

### Code Analysis Storage

Example of storing code analysis results:

```cypher
// Create code file node
CREATE (cf:CodeFile {
  filename: 'user_service.py',
  language: 'python',
  classification: 'Business Logic'
})

// Create data model nodes
CREATE (dm:DataModel {name: 'User', type: 'class'})
CREATE (dm2:DataModel {name: 'UserRepository', type: 'class'})

// Create relationships
CREATE (cf)-[:CONTAINS]->(dm)
CREATE (cf)-[:CONTAINS]->(dm2)
CREATE (dm)-[:USES]->(dm2)
```

### Querying Relationships

```cypher
// Find all data models in a specific file
MATCH (cf:CodeFile {filename: 'user_service.py'})-[:CONTAINS]->(dm:DataModel)
RETURN dm.name, dm.type

// Find dependencies between files
MATCH (cf1:CodeFile)-[:CONTAINS]->(dm1:DataModel)-[:USES]->(dm2:DataModel)<-[:CONTAINS]-(cf2:CodeFile)
WHERE cf1 <> cf2
RETURN cf1.filename, cf2.filename, dm1.name, dm2.name
```

This setup provides a robust foundation for storing and querying your code analysis results in a graph database format.