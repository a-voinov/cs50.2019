from nltk.tokenize import sent_tokenize


def lines(a, b):
    """Return lines in both a and b"""

    result = set()
    a_lines = a.split("\n")
    b_lines = b.split("\n")
    for a_line in a_lines:
        for b_line in b_lines:
            if a_line == b_line:
                result.add(a_line)
    return result


def sentences(a, b):
    """Return sentences in both a and b"""

    result = set()
    # Using sent_tokenize from the Natural Language Toolkit
    a_sentences = sent_tokenize(a)
    b_sentences = sent_tokenize(b)
    for a_sentence in a_sentences:
        if a_sentence in b_sentences:
            result.add(a_sentence)
    return result


def substrings(a, b, n):
    """Return substrings of length n in both a and b"""

    result = set()
    a_subs = []
    b_subs = []
    # Getting substrings of a
    for c in range(len(a)-n+1):
        a_subs.append(a[c:c+n])
    # Getting substrings of b
    for c in range(len(b)-n+1):
        b_subs.append(b[c:c+n])
    # Forming set of substrings
    for a_sub in a_subs:
        if a_sub in b_subs:
            result.add(a_sub)
    return result
