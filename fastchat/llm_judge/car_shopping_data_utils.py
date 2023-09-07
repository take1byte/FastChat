import os
import json
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
        
if __name__ == "__main__":
    dates = ['2023-08-30', '2023-08-31', '2023-09-01', '2023-09-02', '2023-09-03']
    for date in dates:
        input_file = os.path.expandvars(f"$HOME/data/car_shopping_questions_raw_{date}.csv")
        format_questions(input_file, date)