# build_indexes.py

Builds and persists BM25 + Dense (OpenAI embedding) retrieval indexes from a training CSV or HuggingFace dataset. Used for hybrid retrieval in causal QA pipelines (e.g. FinCausal).

---

## Requirements

```bash
pip install pandas llama-index llama-index-embeddings-openai llama-index-retrievers-bm25 PyStemmer datasets
```

---

## Setup

```bash
export OPENAI_API_KEY="sk-..."
```
---

## Usage

### From a local CSV

```bash
python build_indexes.py \
    --train_file train_en.csv \
    --persist_dir ./indexes \
    --language english \
    --embed_model text-embedding-3-small \
    --delimiter ";"
```

### From a HuggingFace dataset

```bash
python build_indexes.py \
    --hf_dataset "your-org/your-dataset" \
    --hf_split train \
    --persist_dir ./indexes \
    --language english \
    --embed_model text-embedding-3-small
```

---

## Arguments

| Argument | Required | Default | Description |
|---|---|---|---|
| `--train_file` | No* | — | Path to local CSV file |
| `--persist_dir` | No | `./indexes` | Directory to save index files |
| `--language` | No | `english` | Language for BM25 stemmer (`english` or `spanish`) |
| `--embed_model` | No | `text-embedding-3-small` | OpenAI embedding model name |
| `--delimiter` | No | `;` | CSV delimiter |
| `--hf_dataset` | No* | — | HuggingFace dataset name (alternative to `--train_file`) |
| `--hf_split` | No | `train` | HuggingFace dataset split |

\* Either `--train_file` or `--hf_dataset` must be provided.

---

## Input Format

CSV (or HuggingFace dataset) must contain these three columns (case-insensitive):

| Column | Description |
|---|---|
| `CONTEXT` | The source passage |
| `QUESTION` | The question over the context |
| `ANSWER` | The gold answer |

---

## Output

Two artifacts saved under `--persist_dir`:

```
indexes/
├── bm25_nodes.pkl       # Pickled TextNode list for BM25 retrieval
└── dense_index/         # LlamaIndex VectorStoreIndex (OpenAI embeddings)
    ├── docstore.json
    ├── index_store.json
    └── vector_store.json
```

---

## Notes

- BM25 index is saved as a raw pickle of `TextNode` objects. Keep your `llama-index` version pinned — unpickling across versions will break.
- Dense index uses OpenAI embeddings — building it costs API credits proportional to dataset size.
- For Spanish data, set `--language spanish` to use the correct stemmer for BM25.
