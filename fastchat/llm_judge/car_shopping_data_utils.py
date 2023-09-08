import os
import argparse
import json
import csv
import pandas as pd

def format_questions(input_file: str, date: str) -> None:
    input_qs = pd.read_csv(input_file, header=0, names=['question', 'reference'])
    qs = input_qs["question"]
    refs = input_qs["reference"]

    with open(f"data/mt_bench/car_questions_{date}.jsonl", 'w') as f:
        row_num = 0
        for q, ref in zip(qs, refs):
            row = json.dumps({"question_id": row_num, "category": "car shopping", "turns": [q], "references": [ref]})
            f.write(row + "\n")
            row_num += 1

def format_question_batches(dates=['2023-08-30', '2023-08-31', '2023-09-01', '2023-09-02', '2023-09-03']):
    for date in dates:
        input_file = os.path.expandvars(f"$HOME/data/car_shopping_questions_raw_{date}.csv")
        format_questions(input_file, date)

def append_question_batches(dates=['2023-08-30', '2023-08-31', '2023-09-01', '2023-09-02', '2023-09-03']):
    row_num = 0
    with open("data/mt_bench/question.jsonl", 'r') as f:
        row_num = sum(1 for _ in f)

    with open("data/mt_bench/question.jsonl", 'a+') as f:
        for date in dates:
            question_batch = f"data/mt_bench/car_questions_{date}.jsonl"
            with open(question_batch, 'r') as qb:
                for line in qb:
                    kvs = json.loads(line)
                    kvs["question_id"] = row_num
                    f.write(json.dumps(kvs) + '\n')
                    row_num += 1

def append_answer_batches(dates=['2023-08-30', '2023-08-31', '2023-09-01', '2023-09-02', '2023-09-03']):
    row_num = 0
    with open("data/mt_bench/model_answer/vicuna-7b-v1.5-car_shopping.jsonl", 'r') as f:
        row_num = sum(1 for _ in f)

    with open("data/mt_bench/model_answer/vicuna-7b-v1.5-car_shopping.jsonl", 'a+') as f:
        for date in dates:
            answer_batch = f"data/mt_bench/model_answer/car_shopping/vicuna-7b-v1.5-car_shopping-{date}.jsonl"
            with open(answer_batch, 'r') as ab:
                for line in ab:
                    kvs = json.loads(line)
                    kvs["question_id"] = row_num
                    f.write(json.dumps(kvs) + '\n')
                    row_num += 1

def generate_batches_for_annotation(dates=['2023-08-30', '2023-08-31', '2023-09-01', '2023-09-02', '2023-09-03']):
    for date in dates:
        question_batch = f"data/mt_bench/car_questions_{date}.jsonl"
        answer_batch = f"data/mt_bench/model_answer/car_shopping/vicuna-7b-v1.5-car_shopping-{date}.jsonl"
        with open(f"data/annotate_us/car_shopping_dialogs_to_annotate_{date}.csv", 'a+') as f:
            csv_writer = csv.writer(f, delimiter=',')
            with open(question_batch, "r") as qb:
                with open(answer_batch, "r") as ab:
                    qs, ans = qb.readlines(), ab.readlines()
                    for (q, a) in zip(qs, ans):
                        q_fields = json.loads(q)
                        a_fields = json.loads(a)
                        csv_writer.writerow([q_fields["question_id"], q_fields["turns"][0], a_fields["choices"][0]["turns"][0]])

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--format-question-batches", type=lambda s: [date.strip() for date in s.split(",")], help="Comma separated list of dates yyyy-mm-dd, e.g., 2023-08-30, 2023-08-31, 2023-09-01. Each date corresponds to a batch of questions collected on that date.")
    parser.add_argument("--append-question-batches", type=lambda s: [date.strip() for date in s.split(",")], help="Comma separated list of dates yyyy-mm-dd, e.g., 2023-08-30, 2023-08-31, 2023-09-01. Each date corresponds to a batch of questions collected on that date.")
    parser.add_argument("--append-answer-batches", type=lambda s: [date.strip() for date in s.split(",")], help="Comma separated list of dates yyyy-mm-dd, e.g., 2023-08-30, 2023-08-31, 2023-09-01.. Each date corresponds to a batch of questions collected on that date.")
    parser.add_argument("--generate-batches-for-annotation", type=lambda s: [date.strip() for date in s.split(",")], help="Comma separated list of dates yyyy-mm-dd, e.g., 2023-08-30, 2023-08-31, 2023-09-01.. Each date corresponds to a batch of questions collected on that date.")

    args = parser.parse_args()

    if args.format_question_batches and len(args.format_question_batches) > 0:
        format_question_batches(dates=args.format_question_batches)

    if args.append_question_batches and len(args.append_question_batches) > 0:
        append_question_batches(dates=args.append_question_batches)

    if args.append_answer_batches and len(args.append_answer_batches) > 0:
        append_answer_batches(dates=args.append_answer_batches)
    
    if args.generate_batches_for_annotation and len(args.generate_batches_for_annotation) > 0:
        generate_batches_for_annotation(dates=args.generate_batches_for_annotation)