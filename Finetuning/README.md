# FinCausal 2026: Multilingual Causal QA Fine-Tuning

This repository contains the pipeline for fine-tuning **GPT-4.1-mini** on the FinCausal 2026 shared task. The project focuses on extractive Question-Answering (QA) to identify financial causal relationships in both **English** and **Spanish**.

## System Structure

| File | Description |
| :--- | :--- |
| `finetune_QA_model.ipynb` | Main Jupyter Notebook for data processing, token counting, and OpenAI job submission. |
| `train.jsonl` | Combined English and Spanish training data in OpenAI Chat format. |
| `eval.jsonl` | Combined development/validation data for performance monitoring. |
| `Dataset/` | Directory containing raw `.csv` files (80/20 split for EN and ES). |

## Technical Workflow

The pipeline automates the following steps:
1. **Data Loading**: Reads multilingual CSVs using `pandas`.
2. **Preprocessing**: Concatenates and shuffles English and Spanish datasets to ensure a balanced multilingual model.
3. **Format Conversion**: Transforms raw text into the `messages` format required by the OpenAI Fine-Tuning API.
4. **Token Validation**: Uses `tiktoken` (encoding `o200k_base`) to estimate costs and verify sequence lengths.
5. **Job Submission**: Uploads files and triggers the supervised fine-tuning job for `gpt-4.1-mini-2025-04-14`.

## Data Specification

The model is trained as a **Causal Analysis Assistant**. It is strictly instructed to extract information **verbatim**.

**ChatML Example:**
```json
{
  "messages": [
    {
      "role": "system", 
      "content": "You are a causal analysis assistant... extract the relevant information verbatim."
    },
    {
      "role": "user", 
      "content": "Context: [Financial Passage]\n\nQuestion: [Causal Inquiry]"
    },
    {
      "role": "assistant", 
      "content": "[Verbatim Extract from Context]"
    }
  ]
}
