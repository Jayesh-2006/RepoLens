# RepoLens

RepoLens is a GraphRAG-powered repository intelligence system that helps developers understand unfamiliar codebases through natural language queries.

It combines **Hybrid Retrieval**, **Cross-Encoder Reranking**, and **Neo4j Knowledge Graph Traversal** to answer questions about repository architecture, implementation details, code relationships, and system behavior.

Instead of manually searching through files, developers can ask questions such as:

```text
What is this repository about?

How does the complete architecture work?

Explain the indexing pipeline.

What does this function do?

Which modules are responsible for retrieval?
```

---

# Why RepoLens?

Understanding large repositories is difficult.

Developers often spend hours:

- Searching across files
- Following function calls
- Tracing dependencies
- Understanding architecture
- Mapping relationships between modules

RepoLens accelerates repository exploration by combining semantic search, lexical search, reranking, and graph-based reasoning into a single retrieval pipeline.

---

# Features

- Hybrid Retrieval (Dense + BM25)
- Reciprocal Rank Fusion (RRF)
- Cross-Encoder Reranking
- AST-Based Code Chunking
- Neo4j Knowledge Graph Construction
- Graph-Aware Retrieval
- Multi-Hop Graph Expansion
- Repository Question Answering
- Python Repository Support
- Persistent ChromaDB Storage

---

# Architecture

## Indexing Pipeline

```text
Repository
    │
    ▼
Repository Loader
    │
    ▼
AST-Based Chunking
    │
    ▼
Embedding Generation
    │
    ├──► ChromaDB
    │
    └──► Graph Analyzer
                │
                ▼
            Neo4j Graph
```

---

## Retrieval Pipeline

```text
User Query
       │
       ▼
 ┌───────────────┐
 │               │
 ▼               ▼
Dense        BM25
Retrieval    Retrieval
 │               │
 └───────┬───────┘
         ▼
Reciprocal Rank Fusion
         │
         ▼
Cross-Encoder Reranking
         │
         ▼
Graph Expansion
         │
         ▼
Final Reranking
         │
         ▼
LLM Answer Generation
```

---

# Knowledge Graph

RepoLens automatically extracts repository entities and relationships.

### Supported Entities

- Classes
- Functions
- Methods
- Variables
- Imports

### Supported Relationships

- CALLS
- IMPORTS
- DEFINES
- CONTAINS

This graph enables graph-aware retrieval and multi-hop repository exploration.

---

# Installation

## Clone RepoLens

```bash
git clone <repo-url>
cd RepoLens
```

## Install Dependencies

```bash
pip install -r requirements.txt
```

## Create Environment File

Create a `.env` file:

```env
NEO4J_URI=neo4j://127.0.0.1:7687
NEO4J_USERNAME=neo4j
NEO4J_PASSWORD=your_password

GROQ_API_KEY=your_groq_api_key
HF_TOKEN=your_huggingface_token
```

---

# Usage

## Step 1: Clone a Repository

```bash
py -m scripts.clone_repo <repo_url> <repo_name>
```

Example:

```bash
py -m scripts.clone_repo https://github.com/user/repo.git my_repo
```

Output:

```text
Repository cloned to: data/repos/my_repo

Next step:
py -m scripts.index_repo my_repo
```

---

## Step 2: Index Repository

```bash
py -m scripts.index_repo my_repo
```

This process:

- Loads repository files
- Generates code chunks
- Creates embeddings
- Stores vectors in ChromaDB
- Builds the Neo4j knowledge graph

Output:

```text
Indexing Complete

Repository: my_repo
{'files': x, 'chunks': y, 'entities': z}

Next step:
py -m scripts.chat my_repo
```

---

## Step 3: Chat with Repository

```bash
py -m scripts.chat my_repo
```

Example:

```text
Query: What is this repository about?

Query: Explain the complete architecture.

Query: How does the forward pass work?

Query: Which modules interact with the vector database?
```

---



# Project Structure

```text
RepoLens
│
├── generation/
│   ├── answer_generator.py
│   └── prompts.py
│
├── graph/
│   ├── graph_analyzer.py
│   ├── graph_builder.py
│   └── neo4j_client.py
│
├── indexing/
│   ├── index_repository.py
│   └── vectordb.py
│
├── ingest/
│   ├── loader.py
│   ├── chunk_documents.py
│   └── chunkers/
│
├── retrievers/
│   ├── dense_retriever.py
│   ├── bm25_retriever.py
│   ├── hybrid_retriever.py
│   ├── graph_retriever.py
│   ├── reranker.py
│   └── rrf.py
│
├── scripts/
│   ├── clone_repo.py
│   ├── index_repo.py
│   └── chat.py
│
├── repolens.py
├── models.py
└── requirements.txt
```

---

# Tech Stack

### Retrieval

- ChromaDB
- BM25
- Reciprocal Rank Fusion (RRF)
- BGE Reranker

### Knowledge Graph

- Neo4j

### LLM

- Groq
- Llama 3.3 70B/ Llama 3.1 8b

### Embeddings

- Sentence Transformers

### Core

- Python
- LangChain

---

# Future Improvements

- Repository Evaluation Framework
- Graph Relationship Weighting
- Adaptive Graph Traversal
- Web-Based Interface
- Multi-Language Repository Support
- Agentic Repository Exploration

---

# License

MIT License

---

