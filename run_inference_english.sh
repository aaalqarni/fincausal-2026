API_KEY="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"
TEMPLATE="./prompts/expert_template.json"
PERSIST_DIR="./indexes/english"
FOLDER="dense_eval_english_expert_template"
FT_JOB="ftjob-PE4hNnl9WAMQu5tpl4uyDBiM"

for SPLIT in validation; do
  for K in 5 10; do
    echo "========================================="
    echo "Running Dense | $SPLIT | shots=$K | FT model"
    echo "========================================="

    mkdir -p "${FOLDER}/${SPLIT}/shots_${K}"
    mkdir -p "debug/${FOLDER}/${SPLIT}/shots_${K}"
    mkdir -p "eval/${FOLDER}/${SPLIT}"

    python inference.py \
      --hf_dataset "Alqarni/fincausal-2026-en" \
      --hf_split $SPLIT \
      --hf_train_split train \
      --api_key "$API_KEY" \
      --template_file "$TEMPLATE" \
      --output_file "${FOLDER}/${SPLIT}/shots_${K}/results_dense_${K}" \
      --debug_file "debug/${FOLDER}/${SPLIT}/shots_${K}/inference.log" \
      --num_shots $K \
      --ft_job_id "$FT_JOB" \
      --use_ft \
      --use_dense \
      --persist_dir "$PERSIST_DIR" \
      --embed_model text-embedding-3-large \
      --eval \
      --sas \
      --eval_save "eval/${FOLDER}/${SPLIT}/eval_dense_${K}.csv"
  done
done

# Summary
echo "split,shots,exact_match,sas" > "${FOLDER}_summary.csv"
for SPLIT in validation; do
  for K in 5 10; do
    EVAL_FILE="eval/${FOLDER}/${SPLIT}/eval_dense_${K}.csv"
    if [ -f "$EVAL_FILE" ]; then
      python -c "
import pandas as pd
df = pd.read_csv('$EVAL_FILE')
em = df['exact_match'].mean()
sas = df['sas_score'].mean() if 'sas_score' in df.columns else 0
print(f'$SPLIT,$K,{em:.4f},{sas:.4f}')
" >> "${FOLDER}_summary.csv"
    fi
  done
done

echo "========================================="
echo "DENSE ENGLISH SUMMARY"
echo "========================================="
column -t -s',' "${FOLDER}_summary.csv"