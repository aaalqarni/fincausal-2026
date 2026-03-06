# FinCausal 2026: RAG Pipeline for Financial Causal QA

This repository contains the code for our system submitted to the **FinCausal 2026** shared task on causal question answering from financial documents.

## Overview

We investigate the effectiveness of fine-tuned generative models combined with **Retrieval-Augmented Generation (RAG)** for verbatim causal extraction from financial texts. Our system compares multiple retrieval strategies for few-shot example selection and evaluates their impact on both base and fine-tuned GPT models.

### Key Findings

- **Fine-tuning is the dominant factor**, nearly doubling exact match scores across both languages.
- **Retrieval strategy has minimal impact after fine-tuning**.
- **RAG benefits are more pronounced for Spanish**, where the base model has weaker zero-shot performance.

---

## Architecture

![System Architecture](Images/FinCausal2026.png)

The pipeline consists of three stages:

1. **Indexing** — Training examples are indexed using multiple retrieval methods.
2. **Retrieval** — Top-k most relevant examples are retrieved for each test query.
3. **Few-shot Prompt Engineering** — Retrieved examples are combined with the test query and passed to the LLM.

---

## Project Structure

```text
.
├── Dataset/                         # Training and evaluation data
├── Finetuning/                      # Fine-tuning scripts and configs
├── Images/                          # Figures and diagrams
├── eval/                            # Evaluation outputs (scores, logs, predictions)
├── indexes/                         # Pre-built retrieval indexes + build scripts
│   ├── build_indexes.py             # Build BM25 + dense indexes
│   └── indexing.sh                  # Index-building shell script
├── prompts/                         # Prompt templates
│   ├── best_template.json           # Best-performing template
│   ├── causal_template.json         # Basic causal extraction
│   ├── expert_template.json         # Domain-expert prompt
│   ├── multilingual_expert.json     # Multilingual expert prompt
│   └── multilingual_expert_cot.json # Multilingual expert + CoT
├── utils/                           # Utility modules
│   ├── __init__.py
│   ├── template.py                  # CAUSE/EFFECT/OTHER classifier
│   ├── evaluation.py                # EM, SAS, partial match metrics
│   ├── retrieval.py                 # Retrieval methods
│   └── data_loader.py               # HuggingFace + CSV data loading
├── inference.py                     # Main inference script
├── run_inference_english.sh         # Example run script (English)
├── requirements.txt                 # Dependencies
├── .gitignore
├── LICENSE
└── README.md
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

### 2. Run Inference
## Inference Example

Run causal QA inference using the hybrid retrieval strategy.

```bash
python inference.py \
 --api_key "sk-..." \                # Required if using OpenAI models (e.g., GPT-4.1)
 --train_file "Dataset/EN/train_80_en.csv" \
 --test_file "Dataset/EN/dev_20_en.csv" \
 --template_file prompts/best_template.json \
 --language english \                # Language used by the BM25 tokenizer (e.g., english, spanish)
 --use_hybrid \                      # Hybrid retrieval (BM25 + Dense)
 --persist_dir ./indexes/english \   # Directory containing the retrieval indexes
 --num_shots 5 \                     # Number of few-shot examples
 --ft_job_id "ftjob-....." \         # Fine-tuned model ID (optional)
 --use_ft \                          # Enable if using a fine-tuned model
 --model gpt-4.1-mini \              # Base model (e.g., GPT-4.1-mini)
 --eval --sas \                      # Run evaluation with SAS scoring
 --output_file eval/results_hybrid_5.csv
```

### Notes

- **Language option**
  - `--language english` → for English datasets  
  - `--language spanish` → for Spanish datasets  
  This ensures the **BM25 parser uses the correct language tokenisation**.

- **Using OpenAI models**
  - Provide `--api_key`
  - Choose the model with `--model`

- **Using a fine-tuned model**
  - Add `--use_ft` and provide the `--ft_job_id`

 - **Model**
  - `gpt-4.1`
  - `gpt-4.1-mini`
  - For the complete list of available OpenAI models, see the official documentation:  
    https://developers.openai.com/api/docs/models
## Evaluation Metrics

| Metric | Description |
|--------|-------------|
| **EM** | Exact Match (case-insensitive string comparison) |
| **SAS** | Semantic Answer Similarity (cosine similarity of sentence embeddings) |
| **LLM** | Official blind test score by LLM-as-judge (1–5 scale) |
