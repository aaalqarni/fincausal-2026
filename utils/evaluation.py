import pandas as pd
from sentence_transformers import SentenceTransformer, util


def eval_report(predictions, gold_answers, partial=False, sas=False, sas_model="all-MiniLM-L6-v2", save_path=None):
    assert len(predictions) == len(gold_answers), "Lengths don't match!"

    sas_scores = None
    if sas:
        model = SentenceTransformer(sas_model)
        pred_embs = model.encode(predictions, convert_to_tensor=True)
        gold_embs = model.encode(gold_answers, convert_to_tensor=True)
        sas_scores = [util.cos_sim(p, g).item() for p, g in zip(pred_embs, gold_embs)]

    results = []
    for i, (pred, gold) in enumerate(zip(predictions, gold_answers)):
        pred_clean = str(pred).strip().lower()
        gold_clean = str(gold).strip().lower()
        row = {
            'index': i,
            'prediction': pred,
            'gold': gold,
            'exact_match': int(pred_clean == gold_clean)
        }
        if partial:
            row['partial_match'] = int(gold_clean in pred_clean or pred_clean in gold_clean)
        if sas:
            row['sas_score'] = round(sas_scores[i], 4)
        results.append(row)

    exact_score = sum(r['exact_match'] for r in results) / len(results)
    print(f"Exact Match: {exact_score:.4f} ({sum(r['exact_match'] for r in results)}/{len(results)})")

    if partial:
        partial_score = sum(r['partial_match'] for r in results) / len(results)
        print(f"Partial Match: {partial_score:.4f}")
    if sas:
        avg_sas = sum(r['sas_score'] for r in results) / len(results)
        print(f"SAS (avg): {avg_sas:.4f}")

    mismatches = [r for r in results if not r['exact_match']]
    if mismatches:
        print(f"\n--- First 5 Mismatches (out of {len(mismatches)}) ---")
        for m in mismatches[:5]:
            print(f"[{m['index']}] PRED: {m['prediction'][:100]}")
            print(f"[{m['index']}] GOLD: {m['gold'][:100]}")
            print()

    if save_path:
        pd.DataFrame(results).to_csv(save_path, index=False)
        print(f"Eval saved to {save_path}")

    return exact_score
