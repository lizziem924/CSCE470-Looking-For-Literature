import math
from collections import defaultdict

class BM25F:
    def __init__(self, fields, k1=1.3):
        # fields = {"description": (FieldIndex, weight, b), "shelves": (...)}
        self.fields, self.k1 = fields, k1
        self.N = next(iter(fields.values()))[0].N

    def idf(self, df):
        return math.log(1 + (self.N - df + 0.5) / (df + 0.5))

    def score(self, query_terms):
        """Return {doc_id: score} for docs containing at least one term."""
        scores = defaultdict(float)
        for term in set(query_terms):
            w = defaultdict(float)                       # doc_id -> w_{d,t} (eq. 3)
            for index, W_f, b_f in self.fields.values():
                for doc_id, tf in index.postings.get(term, {}).items():
                    denom = (1 - b_f) + b_f * index.lengths[doc_id] / (index.avg_len or 1)
                    w[doc_id] += W_f * tf / denom        # eq. 2
            idf = self.idf(len(w))                       # df across all fields
            for doc_id, w_dt in w.items():
                scores[doc_id] += idf * w_dt / (self.k1 + w_dt)   # eq. 4
        return scores