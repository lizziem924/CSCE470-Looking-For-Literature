from collections import Counter, defaultdict

class FieldIndex:
    def __init__(self, token_lists):              # position in list = doc_id
        self.N = len(token_lists)
        self.lengths = [len(t) for t in token_lists]
        self.avg_len = sum(self.lengths) / max(self.N, 1)
        self.postings = defaultdict(dict)         # term -> {doc_id: tf}
        for doc_id, toks in enumerate(token_lists):
            for term, tf in Counter(toks).items():
                self.postings[term][doc_id] = tf