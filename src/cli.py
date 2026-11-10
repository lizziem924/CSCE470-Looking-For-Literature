import argparse
import os
import sys

from data_parsing import load_clean
from search import SearchEngine

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
SAMPLE_PATH = os.path.join(ROOT, "data", "sample_books.jsonl")


def print_results(engine, doc_ids):
    if not doc_ids:
        print("No matching books.")
        return
    for rank, d in enumerate(doc_ids, 1):
        book = engine.books[d]
        authors = ", ".join(book["authors"]) or "(unknown author)"
        extras = [x for x in (book["publisher"], book["isbn13"] or book["isbn"]) if x]
        print(f"{rank:>2}. {book['title']}  --  {authors}")
        print(f"    {' | '.join(extras) if extras else '(no publisher / ISBN)'}"
              f" | text reviews: {book['text_reviews_count']}")


def main():
    p = argparse.ArgumentParser(description="Goodreads book search (BM25)")
    p.add_argument("-q", "--query", default="")
    p.add_argument("--title", default="")
    p.add_argument("--author", default="")
    p.add_argument("--publisher", default="")
    p.add_argument("--isbn", default="")
    p.add_argument("--top-k", type=int, default=5)
    p.add_argument("--data", default=SAMPLE_PATH)
    args = p.parse_args()

    path = args.data
    print("Loading...")
    engine = SearchEngine(load_clean(path))

    bars = (args.query, args.title, args.author, args.publisher, args.isbn)
    if not any(s.strip() for s in bars):
        print("Please have at least one argument (query, title, auther, publisher, or isbn)")
        return
    print_results(engine, engine.search(general=args.query, title=args.title, author=args.author, isbn=args.isbn, publisher=args.publisher, top_k=args.top_k))


if __name__ == "__main__":
    main()