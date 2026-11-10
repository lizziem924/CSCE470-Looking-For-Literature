from collections import defaultdict

import text_tokenizer
from bm25 import BM25F
from index import FieldIndex

K1 = 1.3
# field -> (weight W_f, length-normalization b_f)
TITLE_FIELD = (1.0, 0.3)
AUTHOR_FIELD = (1.0, 0.3)
PUBLISHER_FIELD = (1.0, 0.3)
GENERAL_FIELDS = {"description": (1.0, 0.7), "shelves": (0.5, 0.3)}


def normalize_isbn(text):
    return "".join(ch for ch in text if ch.isalnum()).upper()


class SearchEngine:
    def __init__(self, books, k1=K1):
        self.books = books

        self.title = self._single_field(
            "title", [text_tokenizer.tokenize(b["title"]) for b in books], TITLE_FIELD, k1)
        self.author = self._single_field(
            "authors", [text_tokenizer.tokenize(" ".join(b["authors"])) for b in books], AUTHOR_FIELD, k1)
        self.publisher = self._single_field(
            "publisher", [text_tokenizer.tokenize(b["publisher"]) for b in books], PUBLISHER_FIELD, k1)

        description = FieldIndex([text_tokenizer.tokenize(b["description"]) for b in books])
        shelves = FieldIndex([text_tokenizer.tokenize(" ".join(b["shelves"])) for b in books])
        self.general = BM25F({
            "description": (description, *GENERAL_FIELDS["description"]),
            "shelves": (shelves, *GENERAL_FIELDS["shelves"]),
        }, k1)

        # ISBN is an exact-match field: normalized isbn / isbn13 -> set of doc_ids
        self._isbn_map = defaultdict(set)
        for doc_id, b in enumerate(books):
            for code in (b["isbn"], b["isbn13"]):
                if code.strip():
                    self._isbn_map[normalize_isbn(code)].add(doc_id)

    @staticmethod
    def _single_field(name, token_lists, params, k1):
        weight, b = params
        return BM25F({name: (FieldIndex(token_lists), weight, b)}, k1)

    def isbn_lookup(self, text):
        return {doc_id: 1.0 for doc_id in self._isbn_map.get(normalize_isbn(text), ())}

    def search(self, general="", title="", author="", isbn="", publisher="", top_k=10):
        specific = []                                  # one {doc_id: score} per non-empty bar
        for text, scorer in [(title, self.title), (author, self.author),
                             (publisher, self.publisher)]:
            if text.strip():
                specific.append(scorer.score(text_tokenizer.tokenize(text)))
        if isbn.strip():
            specific.append(self.isbn_lookup(isbn))

        if not specific and not general.strip():
            return []                                  # all bars empty

        if specific:                                   # stage 1: specific bars
            candidates = set.intersection(*(set(s) for s in specific))
            spec = {d: sum(s[d] for s in specific) for d in candidates}
        else:
            candidates, spec = None, {}

        gen = self.general.score(text_tokenizer.tokenize(general)) if general.strip() else {}
        if candidates is None:
            candidates = set(gen)                      # stage 2 only

        def key(d):                                    # general first, then specific, then reviews
            return (round(gen.get(d, 0.0), 6), round(spec.get(d, 0.0), 6),
                    self.books[d]["text_reviews_count"])
        return sorted(candidates, key=key, reverse=True)[:top_k]