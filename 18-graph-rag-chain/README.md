# Module 18: Graph RAG Chain

<!-- lesson:page From Graph Database to Natural Language Answers -->
## From Graph Database to Natural Language Answers

In Modules 16 and 17, we extracted entities and relationships from text using `LLMGraphTransformer` and stored them in a Neo4j database. Now we need to **query** that graph using natural language, just like a user would.

The challenge is bridging two worlds:
- **Users** ask questions in natural language (e.g., "Who contributed to deep learning?")
- **Neo4j** requires Cypher queries to retrieve data

This is analogous to vector RAG, where user queries are embedded into vectors for similarity search. In graph RAG, user queries are translated into **Cypher queries** for graph traversal.

![Graph RAG Architecture](../utils/media/neo4j_rag.png)

### How Does the LLM Know What Cypher to Generate?

The LLM is given access to the **graph schema**, which contains the node types, properties, and relationship types. From this structural information, it can infer which entities and relationships are relevant to the user's question and generate an appropriate Cypher query.

For example, if the schema shows `(:Person)-[:CONTRIBUTED_TO]->(:Technology)`, the LLM knows it can query for contributors to a given technology.

<!-- lesson:page GraphCypherQAChain -->
## GraphCypherQAChain

LangChain provides `GraphCypherQAChain`, a chain that translates natural language questions into Cypher queries, executes them against a Neo4j database, and returns answers in natural language.

### Two Chains Under the Hood

`GraphCypherQAChain` is composed of two sequential chains:

1. **Generate Cypher Chain** - Takes the user's question and the graph schema, then generates a Cypher query
2. **Summarize Results Chain** - Takes the Cypher query results and formats them into a natural language response

### Step 1: Refresh the Graph Schema

Before querying, refresh the schema to ensure the chain has the most up-to-date view of the graph structure. This is particularly useful when the graph is being auto-populated:

```python
graph.refresh_schema()
print(graph.get_schema)
```

### Step 2: Create the Graph RAG Chain

Import `GraphCypherQAChain` and create it using the `.from_llm()` factory method, passing an LLM and the graph database:

```python
from langchain_neo4j import GraphCypherQAChain
from langchain_openai import ChatOpenAI

llm = ChatOpenAI(temperature=0, model="gpt-4o-mini")

chain = GraphCypherQAChain.from_llm(
    llm=llm,
    graph=graph,
    verbose=True
)
```

Setting `verbose=True` lets you see the generated Cypher query and the raw database result in the output, which is helpful for debugging and understanding the chain's behavior.

### Step 3: Ask Questions in Natural Language

Invoke the chain with a natural language query. The chain handles everything: schema inspection, Cypher generation, query execution, and response formatting:

```python
result = chain.invoke({"query": "What technologies are related to neural networks?"})
print(result["result"])
```

Behind the scenes, the chain:
1. Reads the graph schema to understand available node types and relationships
2. Generates a Cypher query like `MATCH (n)-[r]->(m:Technology {id: "Neural Network"}) RETURN n, type(r), m`
3. Executes the query against Neo4j
4. Summarizes the results in natural language

<!-- lesson:page Customizing the Chain -->
## Customizing the Chain

`GraphCypherQAChain` provides several parameters to control its behavior and improve query quality.

### Step 1: Limit Query Results

Use `top_k` to control how many results the Cypher query returns. This prevents overwhelming the LLM with too much data:

```python
chain = GraphCypherQAChain.from_llm(
    llm=llm,
    graph=graph,
    verbose=True,
    top_k=10
)
```

### Step 2: Validate Generated Cypher

Enable `validate_cypher=True` to have the chain check the generated Cypher query before executing it. This catches syntax errors and invalid property references:

```python
chain = GraphCypherQAChain.from_llm(
    llm=llm,
    graph=graph,
    verbose=True,
    validate_cypher=True
)
```

### Step 3: Use Different LLMs for Each Sub-Chain

You can assign separate LLMs to the Cypher generation and answer summarization steps. For example, use a more capable model for generating Cypher and a faster model for summarizing:

```python
cypher_llm = ChatOpenAI(temperature=0, model="gpt-4o")
qa_llm = ChatOpenAI(temperature=0, model="gpt-4o-mini")

chain = GraphCypherQAChain.from_llm(
    cypher_llm=cypher_llm,
    qa_llm=qa_llm,
    graph=graph,
    verbose=True
)
```

When using `cypher_llm` and `qa_llm`, you do not pass the general `llm` parameter.

<!-- lesson:page Key Concepts -->
## Key Concepts

### Summary

| Concept | Description |
|---------|-------------|
| **GraphCypherQAChain** | A chain that converts natural language questions into Cypher queries and returns natural language answers |
| **Generate Cypher Chain** | The first sub-chain that translates user input into a Cypher query using the graph schema |
| **Summarize Results Chain** | The second sub-chain that converts raw query results into a natural language response |
| **refresh_schema()** | Updates the chain's view of the graph structure to reflect recent changes |
| **verbose** | Shows the generated Cypher query and raw results for debugging |
| **validate_cypher** | Checks the generated Cypher for errors before executing it |
| **top_k** | Limits the number of results returned from the Cypher query |
| **cypher_llm / qa_llm** | Allows using different LLMs for Cypher generation and answer summarization |

### Graph RAG vs Vector RAG

| Aspect | Vector RAG | Graph RAG |
|--------|-----------|-----------|
| **Query translation** | Text embedded into vectors | Text translated into Cypher |
| **Retrieval** | Similarity search in vector space | Graph traversal via Cypher |
| **Strengths** | Semantic similarity across large corpora | Relationship-aware, multi-hop reasoning |
| **Best for** | "Find similar content" queries | "How are X and Y related?" queries |

### Key Takeaways

1. `GraphCypherQAChain` bridges natural language and graph databases by generating Cypher queries
2. The chain uses the graph schema to understand available node types and relationships
3. It consists of two sub-chains: one for Cypher generation and one for result summarization
4. `refresh_schema()` ensures the chain has the latest graph structure
5. Use `verbose=True` to inspect generated Cypher queries during development

<!-- lesson:end -->

## Setup

### Prerequisites

- Python 3.10+
- OpenAI API key (set in `.env` file)
- A running Neo4j database with graph data (see Module 17 for setup)

### Running the Example

```bash
make install        # Install Python dependencies
make setup-neo4j    # Start Neo4j (if using Docker)
make run            # Run the example
```

### Dependencies

This module uses:
- `langchain-neo4j` (Neo4jGraph, GraphCypherQAChain)
- `langchain-openai` (ChatOpenAI)
- `langchain-experimental` (LLMGraphTransformer)
- `neo4j` (Neo4j Python driver)
- `wikipedia` (Wikipedia API)
