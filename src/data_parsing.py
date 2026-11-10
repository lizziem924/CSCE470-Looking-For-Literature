import json
import os

OUT_PATH = "data/sample_books.jsonl"

def stream(path):
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            yield json.loads(line)

def load_clean(path=OUT_PATH):
    return list(stream(path))