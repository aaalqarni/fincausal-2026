# FinCausal Prompt Templates

Prompt templates used in our system for the FinCausal 2026 shared task. All templates target **verbatim span extraction** of causal relationships from financial text.

Three prompting strategies were explored: (1) a **simple prompt**, which provides minimal instructions to extract the answer from the context; (2) an **expert prompt**, which assigns the model a domain-expert role and includes detailed extraction rules; and (3) a **multilingual prompt**, which extends the expert prompt with language-aware instructions to handle both English and Spanish inputs.

---

## Templates Overview

| File | Strategy | Language | Notes |
|------|----------|----------|-------|
| `causal_template.json` | Simple prompt | English | Minimal system prompt; extraction rules in user turn |
| `best_template.json` | Simple prompt | English | Best-performing variant; handles parenthetical causal spans |
| `expert_template.json` | Expert prompt | English | Domain-expert role with detailed extraction rules |
| `multingual_expert.json` | Multilingual prompt | English + Spanish | Expert prompt extended with language-aware instructions |
| `multingual_expert_cot.json` | Multilingual prompt + CoT | English + Spanish | **Not used in this work** — reserved for future work |

---

## Template Details

### `causal_template.json` — Simple Prompt
Provides minimal context in the system message (`"You are a causal analysis assistant."`) and places all extraction instructions in the user turn. Represents the simplest prompting strategy with no role assignment or domain framing.

---

### `best_template.json` — Simple Prompt (Best Performing)
Also a simple prompt, but with a richer system message that explicitly handles the edge case where causal information appears inside parentheses between numerical values — a common pattern in financial reporting.

**Key rule:** Treat parenthetical text between two values as explaining the entire change, not just the first value.

---

### `expert_template.json` — Expert Prompt
Assigns the model a domain-expert role (`"You are a causal analysis assistant... given a financial passage"`) and includes detailed, numbered extraction rules. No parenthetical edge-case handling.

---

### `multingual_expert.json` — Multilingual Prompt
Extends the expert prompt with explicit language-aware instructions: `"The passage and question may be in Spanish."` The model is expected to extract verbatim in whichever language the input is written.

---

### `multingual_expert_cot.json` — Multilingual Prompt + CoT *(Not used in this work — reserved for future work)*
Extends the multilingual prompt with a chain-of-thought reasoning step before the final answer. The model must:
1. Identify causal relationships in the passage
2. Locate the exact span
3. Verify it is verbatim

Output format:
```
Reasoning: <step-by-step thinking>
Answer: <verbatim extracted text>
```

---

## Template Format

All templates follow the same JSON schema:

```json
{
  "system_message": "...",
  "user_format": "..."
}
```

The `user_format` field uses two placeholders:

| Placeholder | Description |
|-------------|-------------|
| `{context}` | The financial passage |
| `{question}` | The causal question to answer |


---

## Core Constraint Across All Templates

Every template enforces the same non-negotiable rule: **extract verbatim, output nothing else.** No paraphrasing, no inference, no added explanation. The answer must be a direct span from the input passage.

---

## Prompt Examples

The same passage and question are used across all templates for direct comparison.

**Passage used in examples:**
> We recognise that encouraging greater diversity and more inclusive practices brings benefits to our business, so we have developed a strategy to ensure that we recruit, develop and retain high quality staff irrespective of age, gender, race or sexual orientation.

**Question:** What is the reason for developing a strategy to ensure the recruitment, development, and retention of high-quality staff?

**Expected answer:** `encouraging greater diversity and more inclusive practices brings benefits to our business`

---

### `best_template.json`

#### Zero-shot
```
SYSTEM:
You are a causal analysis assistant. You will be given a passage and a question about causal
relationships. Your task is to answer the question by extracting the relevant information
verbatim from the passage.

RULES:
1. Answer using exact wording from the passage only.
2. Do not paraphrase. Do not infer.
3. When causal information appears in parentheses between two values, it often explains the
   entire change, not just the first value.
4. Output ONLY the extracted text.
5. Do NOT add explanations, notes, or extra content.

USER:
PASSAGE:
We recognise that encouraging greater diversity and more inclusive practices brings benefits
to our business, so we have developed a strategy to ensure that we recruit, develop and retain
high quality staff irrespective of age, gender, race or sexual orientation.

QUESTION:
What is the reason for developing a strategy to ensure the recruitment, development, and
retention of high-quality staff?

ANSWER:

ASSISTANT:
encouraging greater diversity and more inclusive practices brings benefits to our business
```

#### Few-shot
```
SYSTEM:
You are a causal analysis assistant. You will be given a passage and a question about causal
relationships. Your task is to answer the question by extracting the relevant information
verbatim from the passage.

RULES:
1. Answer using exact wording from the passage only.
2. Do not paraphrase. Do not infer.
3. When causal information appears in parentheses between two values, it often explains the
   entire change, not just the first value.
4. Output ONLY the extracted text.
5. Do NOT add explanations, notes, or extra content.

USER:
PASSAGE:
Although our focus is on investing in growth at this stage of the cycle (and shareholders
should thus expect ongoing higher due diligence costs), we will seek to balance this with
continuing to pay a proportion of this growth to our shareholders in the form of progressive
dividends.

QUESTION:
Why should shareholders expect ongoing higher due diligence costs?

ANSWER:

ASSISTANT:
our focus is on investing in growth at this stage of the cycle

USER:
PASSAGE:
Our people are our greatest asset and managing our talent appropriately contributes
significantly to our success.

QUESTION:
What factor accounts for significantly helping their success?

ANSWER:

ASSISTANT:
managing our talent appropriately

USER:
PASSAGE:
We recognise that encouraging greater diversity and more inclusive practices brings benefits
to our business, so we have developed a strategy to ensure that we recruit, develop and retain
high quality staff irrespective of age, gender, race or sexual orientation.

QUESTION:
What is the reason for developing a strategy to ensure the recruitment, development, and
retention of high-quality staff?

ANSWER:

ASSISTANT:
encouraging greater diversity and more inclusive practices brings benefits to our business
```

---

### `causal_template.json`

#### Zero-shot
```
SYSTEM:
You are a causal analysis assistant.

USER:
Context: We recognise that encouraging greater diversity and more inclusive practices brings
benefits to our business, so we have developed a strategy to ensure that we recruit, develop
and retain high quality staff irrespective of age, gender, race or sexual orientation.

Question: What is the reason for developing a strategy to ensure the recruitment,
development, and retention of high-quality staff?

---
INSTRUCTIONS:
1. Extract the answer verbatim from the context above
2. Output ONLY the extracted text
3. Do NOT add: explanations, notes, signatures, emails, or any extra content
4. Your response should contain nothing except the extracted answer
---

 Answer:

ASSISTANT:
encouraging greater diversity and more inclusive practices brings benefits to our business
```

#### Few-shot
```
SYSTEM:
You are a causal analysis assistant.

USER:
Context: Although our focus is on investing in growth at this stage of the cycle (and
shareholders should thus expect ongoing higher due diligence costs), we will seek to balance
this with continuing to pay a proportion of this growth to our shareholders in the form of
progressive dividends.

Question: Why should shareholders expect ongoing higher due diligence costs?

---
INSTRUCTIONS:
1. Extract the answer verbatim from the context above
2. Output ONLY the extracted text
3. Do NOT add: explanations, notes, signatures, emails, or any extra content
4. Your response should contain nothing except the extracted answer
---

 Answer:

ASSISTANT:
our focus is on investing in growth at this stage of the cycle

USER:
Context: Our people are our greatest asset and managing our talent appropriately contributes
significantly to our success.

Question: What factor accounts for significantly helping their success?

---
INSTRUCTIONS:
1. Extract the answer verbatim from the context above
2. Output ONLY the extracted text
3. Do NOT add: explanations, notes, signatures, emails, or any extra content
4. Your response should contain nothing except the extracted answer
---

 Answer:

ASSISTANT:
managing our talent appropriately

USER:
Context: We recognise that encouraging greater diversity and more inclusive practices brings
benefits to our business, so we have developed a strategy to ensure that we recruit, develop
and retain high quality staff irrespective of age, gender, race or sexual orientation.

Question: What is the reason for developing a strategy to ensure the recruitment,
development, and retention of high-quality staff?

---
INSTRUCTIONS:
1. Extract the answer verbatim from the context above
2. Output ONLY the extracted text
3. Do NOT add: explanations, notes, signatures, emails, or any extra content
4. Your response should contain nothing except the extracted answer
---

 Answer:

ASSISTANT:
encouraging greater diversity and more inclusive practices brings benefits to our business
```

---

### `expert_template.json`

#### Zero-shot
```
SYSTEM:
You are a causal analysis assistant. You will be given a financial passage and a question.
Your task is to answer by extracting the relevant information verbatim.

RULES:
1. Extract verbatim only.
2. Output ONLY the extracted text.
3. Do NOT add explanations, notes, or extra content.
4. Output nothing except the answer.

USER:
Context: We recognise that encouraging greater diversity and more inclusive practices brings
benefits to our business, so we have developed a strategy to ensure that we recruit, develop
and retain high quality staff irrespective of age, gender, race or sexual orientation.

Question: What is the reason for developing a strategy to ensure the recruitment,
development, and retention of high-quality staff?

Answer:

ASSISTANT:
encouraging greater diversity and more inclusive practices brings benefits to our business
```

#### Few-shot
```
SYSTEM:
You are a causal analysis assistant. You will be given a financial passage and a question.
Your task is to answer by extracting the relevant information verbatim.

RULES:
1. Extract verbatim only.
2. Output ONLY the extracted text.
3. Do NOT add explanations, notes, or extra content.
4. Output nothing except the answer.

USER:
Context: Although our focus is on investing in growth at this stage of the cycle (and
shareholders should thus expect ongoing higher due diligence costs), we will seek to balance
this with continuing to pay a proportion of this growth to our shareholders.

Question: Why should shareholders expect ongoing higher due diligence costs?

Answer:

ASSISTANT:
our focus is on investing in growth at this stage of the cycle

USER:
Context: Our people are our greatest asset and managing our talent appropriately contributes
significantly to our success.

Question: What factor accounts for significantly helping their success?

Answer:

ASSISTANT:
managing our talent appropriately

USER:
Context: We recognise that encouraging greater diversity and more inclusive practices brings
benefits to our business, so we have developed a strategy to ensure that we recruit, develop
and retain high quality staff irrespective of age, gender, race or sexual orientation.

Question: What is the reason for developing a strategy to ensure the recruitment,
development, and retention of high-quality staff?

Answer:

ASSISTANT:
encouraging greater diversity and more inclusive practices brings benefits to our business
```

---

### `multingual_expert.json`

#### Zero-shot (English)
```
SYSTEM:
You are a causal analysis assistant. You will be given a financial passage and a question.
The passage and question may be in Spanish. Your task is to answer by extracting the relevant
information verbatim.

RULES:
1. Extract verbatim only.
2. Output ONLY the extracted text.
3. Do NOT add explanations, notes, or extra content.
4. Output nothing except the answer.

USER:
Context: We recognise that encouraging greater diversity and more inclusive practices brings
benefits to our business, so we have developed a strategy to ensure that we recruit, develop
and retain high quality staff irrespective of age, gender, race or sexual orientation.

Question: What is the reason for developing a strategy to ensure the recruitment,
development, and retention of high-quality staff?

ASSISTANT:
encouraging greater diversity and more inclusive practices brings benefits to our business
```

#### Zero-shot (Spanish)
```
SYSTEM:
You are a causal analysis assistant. You will be given a financial passage and a question.
The passage and question may be in Spanish. Your task is to answer by extracting the relevant
information verbatim.

RULES:
1. Extract verbatim only.
2. Output ONLY the extracted text.
3. Do NOT add explanations, notes, or extra content.
4. Output nothing except the answer.

USER:
Context: Los ingresos disminuyeron un 12% debido a la caída de los precios del petróleo y a
la reducción de la demanda en los mercados emergentes, lo que obligó a la empresa a revisar
sus proyecciones anuales.

Question: ¿Cuál es la razón de la disminución de los ingresos?

ASSISTANT:
la caída de los precios del petróleo y a la reducción de la demanda en los mercados emergentes
```

#### Few-shot (English + Spanish mixed)
```
SYSTEM:
You are a causal analysis assistant. You will be given a financial passage and a question.
The passage and question may be in Spanish. Your task is to answer by extracting the relevant
information verbatim.

RULES:
1. Extract verbatim only.
2. Output ONLY the extracted text.
3. Do NOT add explanations, notes, or extra content.
4. Output nothing except the answer.

USER:
Context: Our people are our greatest asset and managing our talent appropriately contributes
significantly to our success.
Question: What factor accounts for significantly helping their success?

ASSISTANT:
managing our talent appropriately

USER:
Context: Los ingresos disminuyeron un 12% debido a la caída de los precios del petróleo y a
la reducción de la demanda en los mercados emergentes.
Question: ¿Cuál es la razón de la disminución de los ingresos?

ASSISTANT:
la caída de los precios del petróleo y a la reducción de la demanda en los mercados emergentes

USER:
Context: We recognise that encouraging greater diversity and more inclusive practices brings
benefits to our business, so we have developed a strategy to ensure that we recruit, develop
and retain high quality staff irrespective of age, gender, race or sexual orientation.
Question: What is the reason for developing a strategy to ensure the recruitment,
development, and retention of high-quality staff?

ASSISTANT:
encouraging greater diversity and more inclusive practices brings benefits to our business
```

---

### `multingual_expert_cot.json` *(Not used in this work — reserved for future work)*
```
SYSTEM:
You are a causal analysis assistant. You will be given a financial passage and a question.
The passage and question may be in Spanish.

Think step by step before answering:
1. Identify the causal relationships in the passage.
2. Locate the exact span that answers the question.
3. Verify the span is verbatim from the passage.

RULES:
1. Extract verbatim only.
2. Output ONLY the extracted text after your reasoning.
3. Do NOT add explanations or extra content in the final answer.

Format your response as:
Reasoning: <your step-by-step thinking>
Answer: <verbatim extracted text>

USER:
Context: We recognise that encouraging greater diversity and more inclusive practices brings
benefits to our business, so we have developed a strategy to ensure that we recruit, develop
and retain high quality staff irrespective of age, gender, race or sexual orientation.
Question: What is the reason for developing a strategy to ensure the recruitment,
development, and retention of high-quality staff?

ASSISTANT:
Reasoning:
1. The passage presents a causal structure: "encouraging greater diversity and more inclusive
   practices brings benefits to our business" is the stated cause, connected by "so" to the
   effect of developing a recruitment strategy.
2. The question asks for the reason behind developing the strategy — this maps directly to the
   cause clause before "so".
3. Verbatim span: "encouraging greater diversity and more inclusive practices brings benefits
   to our business" — confirmed present in the passage.

Answer: encouraging greater diversity and more inclusive practices brings benefits to our business
```

#### Few-shot
```
SYSTEM:
You are a causal analysis assistant. You will be given a financial passage and a question.
The passage and question may be in Spanish.

Think step by step before answering:
1. Identify the causal relationships in the passage.
2. Locate the exact span that answers the question.
3. Verify the span is verbatim from the passage.

RULES:
1. Extract verbatim only.
2. Output ONLY the extracted text after your reasoning.
3. Do NOT add explanations or extra content in the final answer.

Format your response as:
Reasoning: <your step-by-step thinking>
Answer: <verbatim extracted text>

USER:
Context: Although our focus is on investing in growth at this stage of the cycle (and
shareholders should thus expect ongoing higher due diligence costs), we will seek to balance
this with continuing to pay a proportion of this growth to our shareholders.
Question: Why should shareholders expect ongoing higher due diligence costs?

ASSISTANT:
Reasoning:
1. The causal signal is "thus" — the cause is the company's focus on investing in growth,
   which leads to higher due diligence costs.
2. The answering span is the clause before "thus": "our focus is on investing in growth at
   this stage of the cycle".
3. Verified verbatim against the passage.

Answer: our focus is on investing in growth at this stage of the cycle

USER:
Context: Our people are our greatest asset and managing our talent appropriately contributes
significantly to our success.
Question: What factor accounts for significantly helping their success?

ASSISTANT:
Reasoning:
1. The causal verb is "contributes" — the cause is "managing our talent appropriately",
   the effect is "our success".
2. The question asks for the contributing factor, so the answer span is the cause.
3. Verbatim span confirmed: "managing our talent appropriately".

Answer: managing our talent appropriately

USER:
Context: We recognise that encouraging greater diversity and more inclusive practices brings
benefits to our business, so we have developed a strategy to ensure that we recruit, develop
and retain high quality staff irrespective of age, gender, race or sexual orientation.
Question: What is the reason for developing a strategy to ensure the recruitment,
development, and retention of high-quality staff?

ASSISTANT:
Reasoning:
1. Causal signal is "so" — the cause precedes it, the effect follows.
2. The cause clause is "encouraging greater diversity and more inclusive practices brings
   benefits to our business".
3. Verified verbatim against the passage.

Answer: encouraging greater diversity and more inclusive practices brings benefits to our business
```