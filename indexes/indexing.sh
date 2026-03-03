export OPENAI_API_KEY="sk-..."

# Use train_en.csv or train_es.csv for the respective language
# Set --language to "english" or "spanish" accordingly
python build_indexes.py \
    --train_file train.csv \
    --persist_dir ./indexes \
    --language english \
    --embed_model text-embedding-3-small \
    --delimiter ";"