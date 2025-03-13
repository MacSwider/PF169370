import re
from collections import Counter


def find_most_frequent_word(text):
    if not text:
        return None

    words = re.findall(r'\b\w+\b', text.lower())
    if not words:
        return None

    count = Counter(words)
    max_count = max(count.values())
    most_frequent_words = [word for word, count in count.items() if count == max_count]

    return most_frequent_words[0]