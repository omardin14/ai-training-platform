# Module 17: Neo4j Graph Store & Cypher Queries

<!-- lesson:page Storing Graph Documents in Neo4j -->
## Storing Graph Documents in Neo4j

In Module 16, we used `LLMGraphTransformer` to extract entities and relationships from text. The next step is to **store** those graph documents in a database so we can query and traverse the relationships.

**Neo4j** is a graph database that comes in both **cloud-based** (Neo4j Aura) and **local** versions to suit different use cases.

### Step 1: Connect to Neo4j (Development)

Use the `Neo4jGraph` class from LangChain to connect to a Neo4j instance. For local development, you can pass credentials directly:

```python
from langchain_neo4j import Neo4jGraph

graph = Neo4jGraph(
    url="bolt://localhost:7687",
    username="neo4j",
    password="your-password"
)
```

### Step 2: Connect Using Environment Variables (Production)

In a production setting, credentials should be stored as environment variables rather than hardcoded in the codebase:

```python
import os

url = os.environ["NEO4J_URI"]
user = os.environ["NEO4J_USERNAME"]
password = os.environ["NEO4J_PASSWORD"]

graph = Neo4jGraph(url=url, username=user, password=password)
```

You can download Neo4j Desktop for local development or sign up for Neo4j Aura (cloud-hosted) at https://neo4j.com/download/

<!-- lesson:page Adding Documents and Viewing the Schema -->
## Adding Graph Documents to the Database

Once connected to Neo4j, we can store the graph documents we created with `LLMGraphTransformer` (from Module 16) into the database.

### Step 1: Add Graph Documents

Use the `.add_graph_documents()` method to store the extracted nodes and relationships:

```python
graph.add_graph_documents(
    graph_documents,
    include_source=True,
    baseEntityLabel=True
)
```

### Parameters Explained

- **`include_source`**: Links each node to its source document by adding a `MENTIONS` relationship in the graph. This creates traceability so you can always trace an entity back to the original text it was extracted from.

- **`baseEntityLabel`**: Assigns an additional `__Entity__` label to every node in the graph. This improves query performance by allowing you to query all entities regardless of their specific type (Person, Technology, Concept, etc.).

### Step 2: View the Database Schema

After adding documents, you can inspect the graph structure using the `.get_schema` attribute:

```python
print(graph.get_schema)
```

This shows the different node types, relationship types, and their directions. For example:

```
Node properties:
  - Person: {id: STRING}
  - Technology: {id: STRING}
  - Concept: {id: STRING}

Relationships:
  - (:Person)-[:CONTRIBUTED_TO]->(:Technology)
  - (:Technology)-[:USES]->(:Concept)
  - (:Person)-[:COLLABORATED_WITH]->(:Person)
```

The schema gives you a quick overview of the graph's structure, showing how different entity types are connected.

<!-- lesson:page Cypher Query Language -->
## Cypher Query Language

**Cypher** is a declarative query language for graph databases, introduced by Neo4j. It uses a SQL-like syntax designed for intuitively navigating and manipulating graph data.

### Step 1: Basic Pattern Matching

The `MATCH` clause finds patterns in the graph. Nodes are represented in parentheses and relationships in square brackets:

```
MATCH (elena:Person {name: "Elena"})
RETURN elena
```

This query finds a node with the label `Person` and the property `name: "Elena"`. The variable `elena` is used to reference the matched node.

### Step 2: Traversing Relationships

Relationships sit between nodes using arrow syntax to indicate direction:

```
MATCH (elena:Person {name: "Elena"})-[:COLLABORATES_WITH]->(colleague)
RETURN colleague
```

This looks for a `Person` node named "Elena" connected to another node via a `COLLABORATES_WITH` relationship. The arrow `->` indicates the direction from Elena to the colleague.

**Key syntax elements:**
- `Person` is the **node label** (the type of entity)
- `{name: "Elena"}` specifies the **property** to match on
- `[:COLLABORATES_WITH]` is the **relationship type**
- `colleague` is a **variable** representing the matched target node

### Step 3: Querying Our Knowledge Graph

Using the graph we built from Wikipedia articles in Module 16, we can query for specific relationships. For example, to find entities that contributed to a technology:

```
MATCH (contributor)-[:CONTRIBUTED_TO]->(tech:Technology {id: "Machine Learning"})
RETURN contributor.id, contributor.type
```

This finds all nodes that have a `CONTRIBUTED_TO` relationship pointing to the "Machine Learning" technology node, and returns their IDs and types.

### More Cypher Examples

Find all relationships for a specific entity:
```
MATCH (n {id: "Neural Network"})-[r]->(target)
RETURN n.id, type(r), target.id
```

Count entities by type:
```
MATCH (n:__Entity__)
RETURN labels(n), count(n)
```

Notice how the `__Entity__` label (from `baseEntityLabel=True`) lets us query all entities regardless of their specific type.

<!-- lesson:page Key Concepts -->
## Key Concepts

### Summary

| Concept | Description |
|---------|-------------|
| **Neo4jGraph** | LangChain's class for connecting to a Neo4j database |
| **add_graph_documents()** | Method to store extracted graph documents in Neo4j |
| **include_source** | Links nodes to their source documents via a MENTIONS relationship |
| **baseEntityLabel** | Adds an `__Entity__` label to all nodes for easier querying |
| **get_schema** | Attribute that shows the graph's node types, relationships, and directions |
| **Cypher** | Neo4j's declarative query language for navigating graph data |
| **MATCH / RETURN** | Core Cypher clauses for finding patterns and returning results |

### When to Use Neo4j

- **Use Neo4j when**: You need persistent storage, complex multi-hop queries, production-grade performance, or collaboration across teams
- **Use in-memory graphs when**: Prototyping, small datasets, or one-off analysis
- **Consider Neo4j Aura (cloud)**: For managed infrastructure without self-hosting

### Key Takeaways

1. `Neo4jGraph` connects LangChain to a Neo4j database for persistent graph storage
2. `.add_graph_documents()` stores extracted entities and relationships from Module 16
3. `include_source` and `baseEntityLabel` improve traceability and query performance
4. Cypher uses pattern matching with `MATCH` and `RETURN` to query graph data
5. The `->` arrow syntax in Cypher represents directional relationships between nodes

<!-- lesson:end -->

## Setup

### Prerequisites

- Python 3.10+
- OpenAI API key (set in `.env` file)
- Docker (for local Neo4j setup) or a Neo4j Aura account (cloud)

### Setting Up Neo4j

#### Option 1: Docker (Recommended)

The easiest way to get Neo4j running locally. One command handles everything:

```bash
make setup-neo4j
```

This will:
1. Pull the latest Neo4j Docker image
2. Start a Neo4j container with pre-configured credentials
3. Expose the web UI at http://localhost:7474
4. Expose the Bolt connection at bolt://localhost:7687

**Default credentials:**
- Username: `neo4j`
- Password: `langchain-training`

Add these to your `.env` file:
```
NEO4J_URI=bolt://localhost:7687
NEO4J_USERNAME=neo4j
NEO4J_PASSWORD=langchain-training
```

**Other Docker commands:**
```bash
make neo4j-status   # Check if Neo4j is running
make stop-neo4j     # Stop and remove the container
```

> **Don't have Docker?** Install it with `brew install --cask docker` (macOS) or visit https://docs.docker.com/get-docker/

#### Option 2: Neo4j Desktop

Download and install Neo4j Desktop from https://neo4j.com/download/

1. Create a new project and database
2. Start the database
3. Note the Bolt URL and credentials
4. Add them to your `.env` file

#### Option 3: Neo4j Aura (Cloud)

Sign up for a free instance at https://neo4j.com/cloud/aura/

1. Create a free AuraDB instance
2. Copy the connection URI, username, and password
3. Add them to your `.env` file

### Running the Example

```bash
make install        # Install Python dependencies
make setup-neo4j    # Start Neo4j (if using Docker)
make run            # Run the example
```

### Dependencies

This module uses:
- `langchain-neo4j` (Neo4jGraph)
- `langchain-experimental` (LLMGraphTransformer)
- `langchain-openai` (ChatOpenAI)
- `neo4j` (Neo4j Python driver)
- `wikipedia` (Wikipedia API)
