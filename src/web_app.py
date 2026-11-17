import json
from functools import partial
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

from data_parsing import load_clean
from search import SearchEngine

ROOT = Path(__file__).resolve().parent.parent
DATA_PATH = ROOT / "data" / "sample_books.jsonl"
UI_PATH = ROOT / "UI"
HOST = "127.0.0.1"
PORT = 8000


class SearchRequestHandler(SimpleHTTPRequestHandler):
    def __init__(self, *args, engine, directory, **kwargs):
        self.engine = engine
        super().__init__(*args, directory=directory, **kwargs)

    def do_POST(self):
        if self.path != "/search":
            self.send_error(404)
            return

        try:
            content_length = int(self.headers.get("Content-Length", "0"))
            if content_length < 0 or content_length > 1_000_000:
                self._send_json(400, {"error": "Invalid request size."})
                return
            payload = json.loads(self.rfile.read(content_length))
        except (ValueError, json.JSONDecodeError):
            self._send_json(400, {"error": "Request must contain valid JSON."})
            return

        if not isinstance(payload, dict):
            self._send_json(400, {"error": "Request must be a JSON object."})
            return

        fields = ("query", "title", "author", "publisher", "isbn")
        if any(not isinstance(payload.get(field, ""), str) for field in fields):
            self._send_json(400, {"error": "Search fields must be strings."})
            return

        top_k_value = payload.get("top_k", "")
        try:
            top_k = int(top_k_value) if str(top_k_value).strip() else 5
        except ValueError:
            self._send_json(400, {"error": "Top K must be a positive whole number."})
            return
        if top_k < 1:
            self._send_json(400, {"error": "Top K must be a positive whole number."})
            return

        doc_ids = self.engine.search(
            general=payload.get("query", ""),
            title=payload.get("title", ""),
            author=payload.get("author", ""),
            publisher=payload.get("publisher", ""),
            isbn=payload.get("isbn", ""),
            top_k=top_k,
        )
        results = []
        for doc_id in doc_ids:
            book = self.engine.books[doc_id]
            results.append({
                "title": book["title"],
                "authors": book["authors"],
                "publisher": book["publisher"],
                "isbn": book["isbn"],
                "isbn13": book["isbn13"],
                "text_reviews_count": book["text_reviews_count"],
            })
        self._send_json(200, {"results": results})

    def _send_json(self, status, payload):
        response = json.dumps(payload).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(response)))
        self.end_headers()
        self.wfile.write(response)


def main():
    engine = SearchEngine(load_clean(str(DATA_PATH)))
    handler = partial(
        SearchRequestHandler,
        engine=engine,
        directory=str(UI_PATH),
    )
    server = ThreadingHTTPServer((HOST, PORT), handler)
    print(f"Serving the search UI at http://{HOST}:{PORT}")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nStopping the search server.")
    finally:
        server.server_close()


if __name__ == "__main__":
    main()
