# Financial Causal Analysis Fine-Tuning

This repository contains a specialized pipeline for fine-tuning Large Language Models to act as **Causal Analysis Assistants**. The goal is to extract verbatim financial causal relationships from provided text passages.

## Repository Structure

* **`finetune_QA_model.ipynb`**: The main notebook containing the training logic, LoRA/QLoRA configuration, and model export steps.
* **`train.jsonl`**: The training set consisting of system, user, and assistant message triplets.
* **`eval.jsonl`**: The validation set used to ensure the model maintains verbatim extraction accuracy without hallucinating or paraphrasing.
* **`README.md`**: Project documentation.



## Data Format

The datasets use the OpenAI-style `messages` format (JSON Lines). Each entry must include a system prompt defining the "Causal Analysis Assistant" persona, a context-heavy user prompt, and a verbatim assistant response.

**Example Entry:**
```jsonl
{
  "messages": [
    {
      "role": "system", 
      "content": "You are a causal analysis assistant... extract information verbatim."
    },
    {
      "role": "user", 
      "content": "Context: Bankia cerró el ejercicio 2018 con un descenso de riesgos del 31% lo que permitió reducir la tasa de morosidad al 6,5%. \n\nQuestion: ¿Por qué se pudo reducir la tasa de morosidad?"
    },
    {
      "role": "assistant", 
      "content": "Bankia cerró el ejercicio 2018 con un elevado descenso de los riesgos dudosos del 31%"
    }
  ]
}