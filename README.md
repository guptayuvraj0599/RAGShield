# RAGShield

### A Poisoning Attack Detection and Defense Framework for Retrieval-Augmented Generation Systems

RAGShield is a security-oriented framework designed to detect and mitigate knowledge-base poisoning attacks in Retrieval-Augmented Generation (RAG) systems.

It introduces a rule-based detection layer between document retrieval and LLM response generation to identify potentially misleading documents before they influence the final response.

## Key Features

- Semantic document retrieval using ChromaDB.
- Document embeddings using Sentence Transformers.
- Controlled generation of synthetic poisoned documents.
- Rule-based poison detection.
- Risk scoring and classification.
- Filtering of potentially harmful retrieved documents.
- Local LLM integration using Ollama and Llama 3.2 (3B).

## Technology Stack

| Component | Technology |
|---|---|
| Programming Language | Python |
| Embedding Model | all-MiniLM-L6-v2 |
| Vector Database | ChromaDB |
| LLM Runtime | Ollama |
| Language Model | Llama 3.2 (3B) |
| Data Storage | JSON |

## Project Architecture

1. Document Processing
2. Embedding Generation
3. Vector Storage
4. Semantic Retrieval
5. Rule-Based Poison Detection
6. Risk Assessment
7. Defense and Context Filtering
8. LLM Response Generation

## Risk Classification

- LOW: Document is allowed.
- MEDIUM: Document is flagged for review and excluded from the permitted context.
- HIGH: Document is blocked.

## Experimental Results

The baseline retrieval experiment was conducted using three test queries.

| Metric | Result |
|---|---:|
| Total Queries | 3 |
| Queries Retrieving Poisoned Documents | 3 |
| Total Retrieved Documents | 9 |
| Poisoned Documents Retrieved | 4 |
| Attack Success Rate | 100% |
| Poison Retrieval Rate | 44.44% |

The rule-based detector flagged all four retrieved poisoned passages in the tested scenarios.

*Note: These results are from a small controlled experiment and should not be interpreted as large-scale benchmark performance.*

## Installation and Execution

Clone the repository:

```bash
git clone YOUR_GITHUB_REPOSITORY_URL
cd RAGShield
```

Create a virtual environment:

```bash
python -m venv .venv
```

Activate it on Windows:

```powershell
.venv\Scripts\activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Run the project using the appropriate setup and execution scripts.

Ollama must be installed separately for local LLM integration.

## Project Team

- Yuvraj Gupta – 23bcs104
- Krish Verma – 23bcs044
- Kartik Sharma – 23bcs038

**Project Guide:** Dr. Rohit Tanwar

**Department:** Computer Science and Engineering

**Institution:** Shri Mata Vaishno Devi University (SMVDU)