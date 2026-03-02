# FinCausal 2026 – Multilingual Causal QA Dataset (English & Spanish)

## Overview

This folder contains the English and Spanish datasets used for training and analysing a multilingual causal question answering (QA) model for the FinCausal 2026 shared task.

The dataset follows an **extractive QA format**. Each sample contains:

- `context` – the financial text passage
- `question` – a causal question about the passage
- `answer` – a verbatim span extracted directly from the context

> **Official dataset source:** [FinCausal 2026 Dataset – e-cienciaDatos](https://edatos.consorciomadrono.es/dataset.xhtml?persistentId=doi:10.21950/H7RKHH)  
> DOI: `10.21950/H7RKHH` — Moreno-Sandoval et al., 2026. Licensed under CC-BY-NC-SA-4.0.

---

## Dataset Structure

| Column | Description |
|--------|-------------|
| `id` | Unique identifier |
| `context` | Financial text passage |
| `question` | Causal question about the passage |
| `answer` | Extracted answer span |

---
## Notebooks

| Notebook | Description |
|----------|-------------|
| `EDA_and_data_splitting.ipynb` | Exploratory data analysis, missing value checks, length statistics, question intent analysis, and 80/20 train–dev split for both EN and ES datasets. |
## Languages & File Structure
```
Datasets/
├── EN/
│   ├── train_en_2000.csv   # Official training set (predefined by organisers)
│   ├── train_en_80.csv     # Internal train split (80% of official train)
│   ├── dev_20_en.csv       # Internal dev split (20% of official train)
│   └── test_en_500.csv     # Official test set
└── ES/
    ├── train_es_2000.csv
    ├── train_es_80.csv
    ├── dev_20_es.csv
    └── test_es_503.csv
```

Both datasets are processed using identical pipelines to ensure structural consistency across languages.

---

## Train–Development Split

`train_en_2000.csv` / `train_es_2000.csv` are the **official training sets** predefined by the FinCausal 2026 organisers.

For internal evaluation, each official training set is further split using a fixed random seed:

| File | Split | Proportion |
|------|-------|------------|
| `train_en_80.csv` / `train_es_80.csv` | Training | 80% |
| `dev_20_en.csv` / `dev_20_es.csv` | Development | 20% |

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

## Preprocessing

The accompanying notebook includes:

- Missing value checks
- Duplicate detection
- Text length statistics
- Sentence segmentation (spaCy)
- Causal signal estimation
- Question intent analysis

---

## Citation

Moreno-Sandoval, A., Torterolo Orta, Y. A., Stanescu, M. A., Chatzi, M. (2026). *The Financial Document Causality Detection Shared Task (FinCausal 2026): Dataset*. e-cienciaDatos. https://doi.org/10.21950/H7RKHH