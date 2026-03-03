"""
Build and persist retrieval indexes (BM25 + Dense).

Usage:
  export OPENAI_API_KEY="sk-..."
  python build_indexes.py \
      --train_file train.csv \
      --persist_dir ./indexes \
      --language english \
      --embed_model text-embedding-3-small \
      --delimiter ";"
"""

import argparse
import os
import pickle
import pandas as pd
from datasets import load_dataset

from llama_index.core import Document, VectorStoreIndex, Settings
from llama_index.core.schema import TextNode
from llama_index.embeddings.openai import OpenAIEmbedding
from llama_index.retrievers.bm25 import BM25Retriever
import Stemmer


def build_nodes(train_df, context_col="CONTEXT", question_col="QUESTION"):
    nodes = []
    for i, row in train_df.iterrows():
        text = f"CONTEXT: {row[context_col]}\nQUESTION: {row[question_col]}"
        node = TextNode(
            text=text,
            metadata={
                "answer": str(row["ANSWER"]),
                "context": str(row[context_col]),
                "question": str(row[question_col]),
                "idx": int(i),
            },
        )
        nodes.append(node)
    return nodes


#def save_bm25_payload(nodes, persist_dir, language="english"):
    """
#    Save the minimal payload needed to rebuild BM25 reliably.
    """
#    bm25_payload = {
#        "language": language,
#        "nodes": nodes,  # TextNode is generally pickle-able; still keep this local + version-pinned.
#    }
#    path = os.path.join(persist_dir, "bm25_nodes.pkl")
#    with open(path, "wb") as f:
#        pickle.dump(bm25_payload, f)
#    print(f"[✅] BM25 payload saved to {path}")

def save_bm25_payload(nodes, persist_dir, language="english"):
    path = os.path.join(persist_dir, "bm25_nodes.pkl")
    with open(path, "wb") as f:
        pickle.dump(nodes, f)
    print(f"[✅] BM25 nodes saved to {path}")

def build_and_save_dense_index(docs, persist_dir, embed_model_name):
    Settings.embed_model = OpenAIEmbedding(model_name=embed_model_name)

    index = VectorStoreIndex.from_documents(docs)
    dense_dir = os.path.join(persist_dir, "dense_index")
    os.makedirs(dense_dir, exist_ok=True)

    index.storage_context.persist(persist_dir=dense_dir)
    print(f"[✅] Dense index saved to {dense_dir}")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--train_file", required=False)
    ap.add_argument("--persist_dir", default="./indexes")
    ap.add_argument("--language", default="english")
    ap.add_argument("--embed_model", default="text-embedding-3-small")
    ap.add_argument("--delimiter", default=";")
    ap.add_argument("--hf_dataset", type=str, default=None, help="HuggingFace dataset name")
    ap.add_argument("--hf_split", type=str, default="train", help="Dataset split")
    args = ap.parse_args()

    if not os.environ.get("OPENAI_API_KEY"):
        raise RuntimeError("OPENAI_API_KEY is not set. Export it instead of passing via CLI.")

    os.makedirs(args.persist_dir, exist_ok=True)
    if args.hf_dataset:
        ds = load_dataset(args.hf_dataset)
        df = ds[args.hf_split].to_pandas()
        df.columns = [c.upper().strip() for c in df.columns]
    else:
        df = pd.read_csv(args.train_file, sep=args.delimiter)
        df.columns = [c.upper().strip() for c in df.columns]

    required = {"CONTEXT", "QUESTION", "ANSWER"}
    missing = required - set(df.columns)
    if missing:
        raise ValueError(f"Missing columns in train file: {sorted(missing)}")

    print(f"[*] Loaded {len(df)} training examples")

    # For dense index, documents are fine
    docs = [
        Document(
            text=f"CONTEXT: {row['CONTEXT']}\nQUESTION: {row['QUESTION']}",
            metadata={
                "answer": str(row["ANSWER"]),
                "context": str(row["CONTEXT"]),
                "question": str(row["QUESTION"]),
                "idx": int(i),
            },
        )
        for i, row in df.iterrows()
    ]

    # For BM25, build nodes (no sentence splitting)
    nodes = build_nodes(df)

    save_bm25_payload(nodes, args.persist_dir, language=args.language)
    build_and_save_dense_index(docs, args.persist_dir, args.embed_model)

    print("\n[✅] All indexes saved:")
    print(f"  - BM25 nodes:   {os.path.join(args.persist_dir, 'bm25_nodes.pkl')}")
    print(f"  - Dense index:  {os.path.join(args.persist_dir, 'dense_index')}")


if __name__ == "__main__":
    main()