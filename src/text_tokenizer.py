import re

STOPWORDS = set("""
a an and are as at be but by for from has have he her his i in is it its of on or
our she that the their them they this to was we were what when which who will with
you your not no so if then than there these those been being do does did can could
would should about into over after before also just more most other some such only
own same too very s t
""".split())


def tokenize(text, remove_stopwords=True):
    if not text:
        return []
    tokens = re.compile(r"[a-z0-9]+").findall(text.lower())
    if remove_stopwords:
        tokens = [t for t in tokens if t not in STOPWORDS]

    return tokens


def content_text(book):
    return (book["description"] + " " + " ".join(book["shelves"])).strip()