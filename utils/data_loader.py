import pandas as pd
from datasets import load_dataset


def load_test_data(args):
    """Load test/dev data from HuggingFace or CSV."""
    ds = None
    if args.hf_dataset:
        ds = load_dataset(args.hf_dataset)
        df = ds[args.hf_split].to_pandas()
        df.columns = [c.upper().strip() for c in df.columns]
    else:
        df = pd.read_csv(args.test_file, sep=args.delimiter)
        df.columns = [c.upper().strip() for c in df.columns]
    return df, ds


def load_train_data(args, ds=None):
    """Load training data from HuggingFace or CSV. Returns HF Dataset or None."""
    # From separate HF repo
    if args.hf_train_dataset:
        train_ds = load_dataset(args.hf_train_dataset)
        train_data = train_ds[args.hf_train_split]
        q_col = "question" if "question" in train_data.column_names else "QUESTION"
        c_col = "context" if "context" in train_data.column_names else "CONTEXT"
        a_col = "answer" if "answer" in train_data.column_names else "ANSWER"
        return train_data, q_col, c_col, a_col

    # From same HF dataset
    if ds and args.hf_train_split and args.hf_train_split in ds:
        train_data = ds[args.hf_train_split]
        q_col = "question" if "question" in train_data.column_names else "QUESTION"
        c_col = "context" if "context" in train_data.column_names else "CONTEXT"
        a_col = "answer" if "answer" in train_data.column_names else "ANSWER"

        # Also save as CSV for random mode
        train_df = train_data.to_pandas()
        train_df.columns = [c.upper().strip() for c in train_df.columns]
        train_df.to_csv("/tmp/train_hf.csv", sep=";", index=False)
        args.train_file = "/tmp/train_hf.csv"

        return train_data, q_col, c_col, a_col

    # From CSV
    if args.train_file:
        train_df = pd.read_csv(args.train_file, sep=args.delimiter)
        train_df.columns = [c.upper().strip() for c in train_df.columns]
        from datasets import Dataset
        train_data = Dataset.from_pandas(train_df)
        return train_data, "QUESTION", "CONTEXT", "ANSWER"

    return None, "QUESTION", "CONTEXT", "ANSWER"
