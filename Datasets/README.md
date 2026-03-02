# FinCausal 2026 – Multilingual Causal QA Dataset (English & Spanish)

## Overview

This folder contains the English and Spanish datasets used for training and analysing a multilingual causal question answering (QA) model for the FinCausal 2026 shared task.

The dataset follows an **extractive QA format**. Each sample contains:

- `context` – the financial text passage
- `question` – a causal question about the passage
- `answer` – a verbatim span extracted directly from the context

---

## Dataset Structure

| Column | Description |
|--------|-------------|
| `id` | Unique identifier |
| `context` | Financial text passage |
| `question` | Causal question about the passage |
| `answer` | Extracted answer span |

---

## Languages

- English
- Spanish

Both datasets are processed using identical pipelines to ensure structural consistency across languages.

---

## Question Types

Questions are categorised using rule-based pattern matching for exploratory analysis:

| Type | Description |
|------|-------------|
| `CAUSE` | Asks for reasons, drivers, or explanations |
| `EFFECT` | Asks for consequences or outcomes |
| `OTHER` | Entailment or implication-based questions |

> This categorisation is used for analysis purposes only.

---

## Key Properties

- Extractive QA format (no paraphrasing)
- Short contexts (typically 2–5 sentences)
- Financial domain
- Balanced causal question distribution

---

## Train–Development Split

Each language dataset is split using a fixed random seed for reproducibility:

| Split | Proportion |
|-------|------------|
| Training | 80% |
| Development | 20% |

---

## Preprocessing

The accompanying notebook includes:

- Missing value checks
- Duplicate detection
- Text length statistics
- Sentence segmentation (spaCy)
- Causal signal estimation
- Question intent analysis