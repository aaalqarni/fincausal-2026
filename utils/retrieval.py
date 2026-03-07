import os
import pickle
import numpy as np
import faiss
import pandas as pd
from collections import defaultdict

from llama_index.core import Document, VectorStoreIndex, Settings, StorageContext, load_index_from_storage
from llama_index.core.node_parser import SentenceSplitter
from llama_index.embeddings.openai import OpenAIEmbedding
from llama_index.retrievers.bm25 import BM25Retriever
import Stemmer

from .template import get_template


# =============================================
# Random
# =============================================
def get_few_shot_messages(train_file, num_shots, context_col, question_col, answer_col, user_fmt, delimiter):
    if num_shots <= 0:
        return []
    train_df = pd.read_csv(train_file, sep=delimiter)
    train_df.columns = [c.upper().strip() for c in train_df.columns]
    samples = train_df.sample(n=num_shots, random_state=42)
    few_shot_messages = []
    for _, row in samples.iterrows():
        user_content = user_fmt.format(context=row[context_col], question=row[question_col])
        few_shot_messages.append({"role": "user", "content": user_content})
        few_shot_messages.append({"role": "assistant", "content": str(row[answer_col])})
    return few_shot_messages


# =============================================
# Dense (LlamaIndex)
# =============================================
def get_dense_few_shot(index, query_text, num_shots, user_fmt, rerank=False, reranker=None):
    if num_shots <= 0:
        return []
    if rerank and reranker:
        retriever = index.as_retriever(similarity_top_k=num_shots * 4)
        results = retriever.retrieve(query_text)
        pairs = [(query_text, r.text) for r in results]
        scores = reranker.predict(pairs)
        results = [r for r, _ in sorted(zip(results, scores), key=lambda x: x[1], reverse=True)[:num_shots]]
    else:
        retriever = index.as_retriever(similarity_top_k=num_shots)
        results = retriever.retrieve(query_text)

    few_shot_messages = []
    for r in results:
        user_content = user_fmt.format(context=r.metadata['context'], question=r.metadata['question'])
        few_shot_messages.append({"role": "user", "content": user_content})
        few_shot_messages.append({"role": "assistant", "content": r.metadata['answer']})
    return few_shot_messages


# =============================================
# BM25
# =============================================
def get_bm25_few_shot(bm25_retriever, query_text, num_shots, user_fmt):
    if num_shots <= 0:
        return []
    bm25_retriever.similarity_top_k = num_shots
    results = bm25_retriever.retrieve(query_text)
    few_shot_messages = []
    for r in results:
        user_content = user_fmt.format(context=r.metadata['context'], question=r.metadata['question'])
        few_shot_messages.append({"role": "user", "content": user_content})
        few_shot_messages.append({"role": "assistant", "content": r.metadata['answer']})
    return few_shot_messages


# =============================================
# Hybrid (BM25 + Dense with RRF)
# =============================================
def get_hybrid_few_shot(bm25_retriever, dense_index, query_text, num_shots, user_fmt, alpha=0.5):
    if num_shots <= 0:
        return []
    k_candidates = num_shots * 3

    bm25_retriever.similarity_top_k = k_candidates
    bm25_results = bm25_retriever.retrieve(query_text)

    dense_retriever = dense_index.as_retriever(similarity_top_k=k_candidates)
    dense_results = dense_retriever.retrieve(query_text)

    rrf_scores = {}
    k_rrf = 60
    for rank, r in enumerate(bm25_results):
        node_id = r.node.node_id
        rrf_scores[node_id] = rrf_scores.get(node_id, {'score': 0, 'node': r})
        rrf_scores[node_id]['score'] += (1 - alpha) * (1 / (k_rrf + rank + 1))
    for rank, r in enumerate(dense_results):
        node_id = r.node.node_id
        rrf_scores[node_id] = rrf_scores.get(node_id, {'score': 0, 'node': r})
        rrf_scores[node_id]['score'] += alpha * (1 / (k_rrf + rank + 1))

    sorted_results = sorted(rrf_scores.values(), key=lambda x: x['score'], reverse=True)[:num_shots]

    few_shot_messages = []
    for item in sorted_results:
        r = item['node']
        user_content = user_fmt.format(context=r.metadata['context'], question=r.metadata['question'])
        few_shot_messages.append({"role": "user", "content": user_content})
        few_shot_messages.append({"role": "assistant", "content": r.metadata['answer']})
    return few_shot_messages


# =============================================
# FAISS Template-Aware
# =============================================
def build_faiss_indexes(train_data, embed_model, q_col="QUESTION", c_col="CONTEXT"):
    clusters = defaultdict(list)
    for i in range(len(train_data)):
        t = get_template(str(train_data[i][q_col]))
        clusters[t].append(i)

    print(f"[*] Template counts: { {k: len(v) for k, v in clusters.items()} }")

    indices = {}
    id_maps = {}

    for t, row_ids in clusters.items():
        docs = []
        for rid in row_ids:
            ex = train_data[rid]
            docs.append(f"Context: {ex[c_col]}\nQuestion: {ex[q_col]}")

        embs = embed_model.encode(
            [f"passage: {d}" for d in docs],
            batch_size=64,
            show_progress_bar=True,
            normalize_embeddings=True,
        ).astype("float32")

        dim = embs.shape[1]
        ix = faiss.IndexFlatIP(dim)
        ix.add(embs)

        indices[t] = ix
        id_maps[t] = np.array(row_ids, dtype=np.int64)
        print(f"Built FAISS index for {t}: {ix.ntotal} vectors")

    return indices, id_maps, clusters


def save_faiss_indexes(indices, id_maps, persist_dir):
    os.makedirs(persist_dir, exist_ok=True)
    for t in indices:
        faiss.write_index(indices[t], os.path.join(persist_dir, f"faiss_{t}.index"))
        np.save(os.path.join(persist_dir, f"idmap_{t}.npy"), id_maps[t])
    print(f" FAISS indexes saved to {persist_dir}")


def load_faiss_indexes(persist_dir):
    indices = {}
    id_maps = {}
    for f in os.listdir(persist_dir):
        if f.startswith("faiss_") and f.endswith(".index"):
            t = f.replace("faiss_", "").replace(".index", "")
            indices[t] = faiss.read_index(os.path.join(persist_dir, f))
            id_maps[t] = np.load(os.path.join(persist_dir, f"idmap_{t}.npy"))
            print(f" Loaded FAISS index for {t}: {indices[t].ntotal} vectors")
    return indices, id_maps


def get_faiss_few_shot(indices, id_maps, train_data, embed_model, context, question, num_shots, user_fmt,
                       q_col="QUESTION", c_col="CONTEXT", a_col="ANSWER"):
    if num_shots <= 0:
        return [], "NONE"

    t = get_template(question)
    if (t not in indices) or (indices[t].ntotal < num_shots):
        fallback = "OTHER" if "OTHER" in indices else list(indices.keys())[0]
        t = fallback

    query_text = f"Context: {context}\nQuestion: {question}"
    q_emb = embed_model.encode(
        [f"query: {query_text}"],
        show_progress_bar=False,
        normalize_embeddings=True,
    ).astype("float32")

    top_n = min(num_shots * 4, indices[t].ntotal)
    scores, local_idx = indices[t].search(q_emb, top_n)
    row_ids = id_maps[t][local_idx[0]]

    few_shot_messages = []
    for rid in row_ids[:num_shots]:
        ex = train_data[int(rid)]
        user_content = user_fmt.format(context=ex[c_col], question=ex[q_col])
        few_shot_messages.append({"role": "user", "content": user_content})
        few_shot_messages.append({"role": "assistant", "content": str(ex[a_col])})

    return few_shot_messages, t
