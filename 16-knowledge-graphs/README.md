# Module 16: Knowledge Graphs

<!-- lesson:page Limitations of Vector Store RAG -->
## Limitations of Vector Store RAG

While vector stores are a powerful tool for retrieval-augmented generation, they come with notable limitations:

### 1. Semantic Meaning Only

Document embeddings capture **semantic similarity** but struggle to represent **themes and relationships** between entities across a document corpus. For example, a vector store may find documents about "machine learning" and "neural networks" separately, but it cannot inherently model the relationship that neural networks are a *subset* of machine learning techniques.

### 2. Scaling Challenges

As the volume of data in a vector database grows, the retrieval process can become **less efficient**. The computational load increases with the search space, making queries slower and more resource-intensive at scale.

### 3. Structured and Diverse Data

Vector-based RAG systems don't easily accommodate **structured or diverse data types**. Tabular data, hierarchical relationships, and multi-modal information are harder to embed meaningfully into a single vector space.

These limitations motivate the use of **graph-based approaches**, which can model complex relationships natively.

<!-- lesson:page Why Graphs? -->
## Why Graphs?

Graphs are excellent at representing and storing **diverse and interconnected information** in a structured manner.

### Nodes

Entities like people, organizations, concepts, and technologies are represented as **nodes**. Each node can contain any number of properties stored as key-value pairs.

```
Node(id="Python", type="Programming Language", properties={"year": 1991})
Node(id="Guido van Rossum", type="Person", properties={"role": "Creator"})
```

### Edges (Relationships)

Connections between entities are represented as **labeled edges**. Edges are **directional**, meaning a relationship can apply from one entity to another, but not necessarily the other way around.

```
Relationship(
    source=Node(id="Guido van Rossum"),
    target=Node(id="Python"),
    type="CREATED"
)
```

In this example, "Guido van Rossum" CREATED "Python", but not the reverse.

Here is an example of a knowledge graph with multiple node types and relationships:

![Graph Nodes and Edges](../utils/media/graph_node_edges.png)

Notice how the graph captures different entity types (actors, movies, awards, studios) and the directional relationships between them. This is something a flat vector store cannot represent.

### Neo4j

**Neo4j** is a powerful graph database designed to store and efficiently query complex relationships. It uses the Cypher query language and is widely used for knowledge graphs, recommendation engines, and fraud detection.

LangChain provides integrations with Neo4j for building graph-based RAG applications.

<!-- lesson:page From Text to Graph -->
## From Text to Graph

How do we go from unstructured text data to a structured knowledge graph? LangChain provides a pipeline for this transformation.

### Step 1: Load and Split Documents

First, load source documents and split them into manageable chunks. For example, using Wikipedia as a source:

```python
from langchain_community.document_loaders import WikipediaLoader
from langchain_text_splitters import TokenTextSplitter

raw_documents = WikipediaLoader(query="Machine Learning").load()
text_splitter = TokenTextSplitter(chunk_size=100, chunk_overlap=20)
documents = text_splitter.split_documents(raw_documents[:3])
```

### Step 2: Create the Graph Transformer

Define the LLM and use it to create an `LLMGraphTransformer`, which extracts entities and relationships from text:

```python
from langchain_openai import ChatOpenAI
from langchain_experimental.graph_transformers import LLMGraphTransformer

llm = ChatOpenAI(temperature=0, model="gpt-4o-mini")
llm_transformer = LLMGraphTransformer(llm=llm)
```

### Step 3: Transform Documents

The LLM parses each document, identifies entities, and infers relationships between them:

```python
graph_documents = llm_transformer.convert_to_graph_documents(documents)
```

### Step 4: Inspect the Output

The result is a list of `GraphDocument` objects containing nodes and relationships:

```python
GraphDocument(
    nodes=[
        Node(id='Neural Network', type='Technology'),
        Node(id='Deep Learning', type='Concept'),
        Node(id='Geoffrey Hinton', type='Person'),
    ],
    relationships=[
        Relationship(
            source=Node(id='Deep Learning'),
            target=Node(id='Neural Network'),
            type='USES'
        ),
    ]
)
```

The model infers entities from the text and creates typed nodes with IDs. Relationships between entities are also inferred and mapped as directional edges.

<!-- lesson:page Key Concepts -->
## Key Concepts

### Summary

| Concept | Description |
|---------|-------------|
| **Node** | An entity (person, concept, technology) with an ID, type, and properties |
| **Edge / Relationship** | A directional connection between two nodes with a label |
| **Knowledge Graph** | A structured representation of entities and their relationships |
| **Neo4j** | A graph database for storing and querying relationship data |
| **LLMGraphTransformer** | Uses an LLM to extract entities and relationships from text |
| **GraphDocument** | LangChain's output format containing nodes and relationships |

### When to Use Graphs vs Vectors

- **Vector stores**: Best for semantic similarity search over large text corpora
- **Knowledge graphs**: Best when relationships between entities matter, or when data is structured and interconnected
- **Hybrid**: Combine both approaches for the most comprehensive RAG system

### Key Takeaways

1. Vector stores capture meaning but miss relationships between entities
2. Graphs model entities as nodes and relationships as directional edges
3. `LLMGraphTransformer` automates the extraction of graph structures from text
4. Neo4j provides a production-ready graph database for storing these relationships

<!-- lesson:end -->

## Setup

### Prerequisites

- Python 3.10+
- OpenAI API key (set in `.env` file)

### Running the Example

```bash
make run
```

### Dependencies

This module uses:
- `langchain-community` (WikipediaLoader)
- `langchain-experimental` (LLMGraphTransformer)
- `langchain-openai` (ChatOpenAI)
- `wikipedia` (Wikipedia API)
