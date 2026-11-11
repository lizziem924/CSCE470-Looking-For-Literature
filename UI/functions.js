function accept_input() {
    let general_query = document.getElementById("query_input").value;
    let title = document.getElementById("title_input").value;
    let author = document.getElementById("author_input").value;
    let publisher = document.getElementById("publisher_input").value;
    let isbn = document.getElementById("isbn_input").value;
    let topk = document.getElementById("topk_input").value;

    document.getElementById("results_output").textContent = 
    "python src/cli.py --query " + general_query + 
    " --title " + title + " --author " + 
    " --publisher " + publisher + 
    " --isbn " + isbn +
    " --top-k " + topk;
}