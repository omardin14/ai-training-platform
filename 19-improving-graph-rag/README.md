# Module 19: Improving Graph RAG Architecture

<!-- lesson:page Limitations of Basic Graph RAG -->
## Limitations of Basic Graph RAG

In Module 18, we built a Graph RAG chain using `GraphCypherQAChain` to translate natural language questions into Cypher queries. While this works well for straightforward questions, the main limitation is the **reliability of the Cypher query generation**.

LLMs can struggle with:
- **Irrelevant node types** cluttering the schema and confusing the model
- **Relationship directions** — LLMs often generate incorrect arrow directions in Cypher
- **Complex queries** — Without guidance, the model may produce syntactically valid but logically incorrect Cypher

This module covers three techniques to improve Graph RAG reliability:

1. **Filtering** — Reduce the schema surface area by excluding irrelevant node types
2. **Cypher Validation** — Automatically detect and fix relationship direction errors
3. **Few-Shot Prompting** — Guide the model with example question-to-Cypher pairs

<!-- lesson:page Filtering the Graph Schema -->
## Filtering the Graph Schema

The first technique is to **filter down the search space** by excluding node types that are not relevant to your use case. A smaller, more focused schema helps the LLM generate more accurate Cypher queries.

### Step 1: Review the Current Schema

Before filtering, inspect the full schema to identify which node types are relevant:

```python
graph.refresh_schema()
print(graph.get_schema)
```

You might see node types like `Document`, `Chunk`, or `Concept` that were created during ingestion but are not useful for answering user questions.

### Step 2: Exclude Irrelevant Node Types

Use the `exclude_types` argument in `.from_llm()` to remove specific node types from the schema the LLM sees:

```python
from langchain_neo4j import GraphCypherQAChain
from langchain_openai import ChatOpenAI

llm = ChatOpenAI(temperature=0, model="gpt-4o-mini")

chain = GraphCypherQAChain.from_llm(
    graph=graph,
    llm=llm,
    exclude_types=["Concept"],
    verbose=True,
    allow_dangerous_requests=True
)
```

With `exclude_types=["Concept"]`, any nodes labeled `Concept` and their relationships are hidden from the schema. The LLM only sees the remaining node types, reducing confusion and improving query accuracy.

### Step 3: Verify the Filtered Schema

After creating the chain, you can check what the LLM actually sees by printing the schema:

```python
print(graph.get_schema)
```

The excluded node types and their relationships will no longer appear in the output.

<!-- lesson:page Validating Cypher Queries -->
## Validating Cypher Queries

LLMs have particular difficulty inferring the **direction of relationships** when generating Cypher statements. For example, the model might generate `(a)-[:WORKS_AT]->(b)` when the actual schema has the relationship going the other way.

### How Validation Works

After the Cypher is generated, `validate_cypher` checks the query against the graph schema through four steps:

1. **Detects nodes and relationships** in the generated Cypher query
2. **Determines the direction** of each relationship in the query
3. **Checks the graph schema** to verify node labels and relationship types
4. **Updates the direction** of relationships to match the schema

### Step 1: Enable Cypher Validation

Add `validate_cypher=True` to the chain configuration:

```python
chain = GraphCypherQAChain.from_llm(
    graph=graph,
    llm=llm,
    verbose=True,
    validate_cypher=True,
    allow_dangerous_requests=True
)
```

### Step 2: Test with a Query

When you invoke the chain with `verbose=True`, you can observe the generated Cypher before and after validation:

```python
result = chain.invoke({"query": "What technologies use neural networks?"})
print(result["result"])
```

If the LLM generates a relationship with the wrong direction, the validator will automatically correct it before the query reaches Neo4j.

<!-- lesson:page Few-Shot Prompting for Cypher -->
## Few-Shot Prompting for Cypher

The most powerful technique is **few-shot prompting**: providing the model with example pairs of user questions and their corresponding Cypher queries. This guides the model toward correct query patterns for your specific graph structure.

### Step 1: Define Example Question-Cypher Pairs

Create a list of examples that demonstrate the query patterns relevant to your knowledge graph:

```python
examples = [
    {
        "question": "How many distinct technologies are mentioned in the graph?",
        "query": "MATCH (t:Technology) RETURN count(DISTINCT t) AS total",
    },
    {
        "question": "Which people have contributed to machine learning research?",
        "query": "MATCH (p:Person)-[:CONTRIBUTED_TO]->(t:Technology {id: 'Machine Learning'}) RETURN DISTINCT p.id",
    },
    {
        "question": "What relationships does a specific technology have?",
        "query": "MATCH (t:Technology {id: 'Neural Network'})-[r]->(target) RETURN t.id, type(r), target.id",
    },
]
```

### Step 2: Create the Example Prompt Template

Define a template that structures each example consistently. This tells the model the expected format for input and output:

```python
from langchain_core.prompts import FewShotPromptTemplate, PromptTemplate

example_prompt = PromptTemplate.from_template(
    "User input: {question}\nCypher query: {query}"
)
```

### Step 3: Build the Few-Shot Prompt

Combine the examples, template, and instructions into a `FewShotPromptTemplate`:

```python
cypher_prompt = FewShotPromptTemplate(
    examples=examples,
    example_prompt=example_prompt,
    prefix=(
        "You are a Neo4j expert. Given an input question, create a "
        "syntactically correct Cypher query to run.\n\n"
        "Here is the schema information\n{schema}.\n\n"
        "Below are a number of examples of questions and their "
        "corresponding Cypher queries."
    ),
    suffix="User input: {question}\nCypher query: ",
    input_variables=["question"],
)
```

The `prefix` provides context and the schema placeholder. The `suffix` is where the actual user question goes.

### Step 4: Use the Custom Prompt in the Chain

Pass the few-shot prompt to `GraphCypherQAChain` via the `cypher_prompt` parameter:

```python
chain = GraphCypherQAChain.from_llm(
    graph=graph,
    llm=llm,
    cypher_prompt=cypher_prompt,
    verbose=True,
    validate_cypher=True,
    allow_dangerous_requests=True
)
```

By combining `cypher_prompt` with `validate_cypher`, you get both guided query generation and automatic direction correction — the most robust configuration for production use.

<!-- lesson:page Key Concepts -->
## Key Concepts

### Summary

| Concept | Description |
|---------|-------------|
| **exclude_types** | Removes specified node types from the schema the LLM sees, reducing confusion |
| **validate_cypher** | Automatically checks and corrects relationship directions in generated Cypher |
| **Few-Shot Prompting** | Provides example question-to-Cypher pairs to guide the model's query generation |
| **FewShotPromptTemplate** | LangChain class for building prompts with example pairs |
| **cypher_prompt** | Parameter to pass a custom prompt template to GraphCypherQAChain |
| **Schema filtering** | Reduces the search space to improve LLM accuracy on Cypher generation |

### Techniques Comparison

| Technique | What It Fixes | When to Use |
|-----------|--------------|-------------|
| **Filtering** | Irrelevant node types confusing the model | Large graphs with many node types not needed for queries |
| **Cypher Validation** | Incorrect relationship directions | Always — low cost, high value safety net |
| **Few-Shot Prompting** | Complex or domain-specific query patterns | When the model struggles with your specific graph structure |

### Key Takeaways

1. `exclude_types` narrows the schema to only relevant node types
2. `validate_cypher=True` catches and corrects relationship direction errors automatically
3. Few-shot prompting guides the LLM with example question-to-Cypher pairs
4. Combining all three techniques creates the most reliable Graph RAG pipeline
5. Always use `verbose=True` during development to inspect generated Cypher queries

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
- `langchain-core` (FewShotPromptTemplate, PromptTemplate)
- `langchain-experimental` (LLMGraphTransformer)
- `neo4j` (Neo4j Python driver)
- `wikipedia` (Wikipedia API)
