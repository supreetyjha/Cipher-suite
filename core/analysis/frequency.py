from collections import Counter


def analyze(text: str) -> dict[str, float]:
    letters = [c.upper() for c in text if c.isalpha()]
    if not letters:
        return {}

    total = len(letters)
    counts = Counter(letters)
    return {letter: round((count / total) * 100, 2) for letter, count in sorted(counts.items())}