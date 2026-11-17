async function accept_input() {
    const output = document.getElementById("results_output");
    output.textContent = "Searching...";

    const search = {
        query: document.getElementById("query_input").value,
        title: document.getElementById("title_input").value,
        author: document.getElementById("author_input").value,
        publisher: document.getElementById("publisher_input").value,
        isbn: document.getElementById("isbn_input").value,
        top_k: document.getElementById("topk_input").value
    };

    try {
        const response = await fetch("/search", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(search)
        });
        const data = await response.json();
        if (!response.ok) {
            throw new Error(data.error || "The search request failed.");
        }

        output.textContent = data.results.length
            ? data.results.map((book, index) => {
                const authors = book.authors.length
                    ? book.authors.join(", ")
                    : "(unknown author)";
                const identifiers = [book.publisher, book.isbn13 || book.isbn]
                    .filter(Boolean);
                const details = identifiers.length
                    ? identifiers.join(" | ")
                    : "(no publisher / ISBN)";
                return `${index + 1}. ${book.title} -- ${authors}\n` +
                    `   ${details} | text reviews: ${book.text_reviews_count}`;
            }).join("\n\n")
            : "No matching books.";
    } catch (error) {
        output.textContent = `Search failed: ${error.message}`;
        console.error(error);
    }
}