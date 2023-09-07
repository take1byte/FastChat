declare -a dates=("2023-08-31" "2023-09-01" "2023-09-02" "2023-09-03")

for date in "${dates[@]}"
do
    cp data/mt_bench/car_questions_${date}.jsonl data/mt_bench/question.jsonl
    echo "processing" `wc -l data/mt_bench/question.jsonl` "questions from $date"
    python3 gen_model_answer.py --model-path lmsys/vicuna-7b-v1.5 --model-id vicuna-7b-v1.5-car_shopping-$date --load-8bit
done