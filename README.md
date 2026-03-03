Here is the corrected and integrated `README.md` content in Markdown format. I have cleaned up the structure, fixed the spelling errors, and properly formatted the system overview.

```markdown
# FinCausal 2026: RAG Pipeline for Financial Causal QA

This repository contains the code for a system submitted to the **FinCausal 2026** shared task on causal question answering from financial documents.

## Overview

We investigate the effectiveness of fine-tuned generative models combined with **Retrieval-Augmented Generation (RAG)** for verbatim causal extraction from financial texts. Our system compares multiple retrieval strategies for few-shot example selection and evaluates their impact on both base and fine-tuned GPT models.

### Key Findings
- **Fine-tuning is the dominant factor**, nearly doubling exact match scores across both languages.
- **Retrieval strategy has minimal impact after fine-tuning**, with all methods yielding comparable results (EM variance < 2%).
- **RAG benefits are more pronounced for Spanish**, where the base model has weaker zero-shot performance.

---

## Architecture



The pipeline consists of three stages:
1. **Indexing** — Training examples are indexed using multiple retrieval methods.
2. **Retrieval** — Top-k most relevant examples are retrieved for each test query.
3. **Few-shot Prompt Engineering** — Retrieved examples are combined with the test query and passed to the LLM.

---

## Project Structure

```text
├── Dataset/                   # Raw training and evaluation CSV data
├── Finetuning/                # Notebooks and scripts for GPT-4.1-mini tuning
├── Images/                    # Figures and architectural diagrams
├── eval/                      # Output logs and evaluation results
├── indexes/                   # Persisted BM25 (.pkl) and Dense Vector indexes
├── prompts/                   # Prompt templates for different RAG strategies
│   ├── best_template.json     # Top-performing prompt configuration
│   ├── causal_template.json   # Basic causal extraction logic
│   ├── expert_template.json   # Financial domain-expert persona
│   ├── multilingual_expert.json # Fixed spelling
│   └── multilingual_expert_cot.json # Fixed spelling
├── utils/                     # Core logic modules
│   ├── __init__.py
│   ├── template.py            # CAUSE/EFFECT/OTHER classification logic
│   ├── evaluation.py          # Metrics: Exact Match (EM), SAS, Partial Match
│   ├── retrieval.py           # Hybrid (BM25 + Vector) retrieval implementation
│   └── data_loader.py         # Script for CSV and local data handling
├── .gitignore                 # Prevents pushing indexes and keys to GitHub
├── build_indexes.py           # Script to build BM25 + Dense indexes
├── indexing.sh                # Automation script for index generation
├── inference.py               # Main RAG inference and generation script
├── run_inference_english.sh   # Execution script for English pipeline
├── requirements.txt           # Project dependencies
├── LICENSE                    # Project license
└── README.md                  # Project documentation

```

---

## Installation

```bash
pip install -r requirements.txt

```

## Usage

### 1. Build Indexes

Ensure your `OPENAI_API_KEY` is exported in your environment.

```bash
export OPENAI_API_KEY="sk-..."

# English
python build_indexes.py \
  --train_file "Dataset/EN/train_80_en.csv" \
  --persist_dir ./indexes/english \
  --language english \
  --embed_model text-embedding-3-large

# Spanish
python build_indexes.py \
  --train_file "Dataset/ES/train_80_es.csv" \
  --persist_dir ./indexes/spanish \
  --language spanish \
  --embed_model text-embedding-3-large

```

### 2. Run Inference (Example)

**Hybrid retrieval with fine-tuned model:**

```bash
python inference.py \
  --train_file "Dataset/EN/dev_20_en.csv" \
  --template_file prompts/best_template.json \
  --use_hybrid \
  --persist_dir ./indexes/english \
  --num_shots 5 \
  --use_ft \
  --eval --sas \
  --output_file eval/results_hybrid_5.csv

```

---

## Evaluation Metrics

* **EM** — Exact Match (case-insensitive string comparison)
* **SAS** — Semantic Answer Similarity (cosine similarity of sentence embeddings)
* **LLM** — Official blind test score by LLM-as-judge (1–5 scale)

```
