# CSCE470-Looking-For-Literature

To run the code, you must run this command:\
python src/cli.py --query "<query>" --title "<title_name>" --author "<author_name>" --publisher "<publisher_name>" --isbn "<isbn>" --top-k &lt;k&gt;

For example:\
python src/cli.py --query "young adult books" --title "Half Bad (Half Life, #1)" --author "Sally Green" --publisher "Viking Children's" --isbn "9780698143760" --top-k 1

You can leave out any fields, but you must have at least one of the following: query, title, author, publisher, or isbn. Some examples are:\
python src/cli.py --query "heaven" --top-k 4\
python src/cli.py --isbn "9786026657534"\
python src/cli.py --title "World History"


Dataset Citations\
Mengting Wan, Julian McAuley, "Item Recommendation on Monotonic Behavior Chains", in RecSys'18. [bibtex]
Mengting Wan, Rishabh Misra, Ndapa Nakashole, Julian McAuley, "Fine-Grained Spoiler Detection from Large-Scale Review Corpora", in ACL'19. [bibtex]
