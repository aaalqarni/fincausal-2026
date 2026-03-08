API_KEY="sk-"
TEMPLATE="./prompts/expert_template.json"
PERSIST_DIR="./indexes/english"
FOLDER="dense_eval_english_expert_template"
FT_JOB="ftjob-........"

for SPLIT in validation; do
  for K in 5 10; do
    echo "========================================="
    echo "Running Dense | $SPLIT | shots=$K | FT model"
    echo "========================================="

    mkdir -p "${FOLDER}/${SPLIT}/shots_${K}"
    mkdir -p "debug/${FOLDER}/${SPLIT}/shots_${K}"
    mkdir -p "eval/${FOLDER}/${SPLIT}"

    python inference.py \
      --train_file "Dataset/EN/train_80_en.csv" \
      --test_file "Dataset/EN/dev_20_en.csv" \
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


echo "========================================="
echo "DENSE ENGLISH SUMMARY"
echo "========================================="
column -t -s',' "${FOLDER}_summary.csv"
