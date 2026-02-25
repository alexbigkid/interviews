"""Most Common Word."""

# Standard imports
import re
from collections import Counter
import logging

from src.shared.performance_timer import PerformanceTimer


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def most_common_word_v1(paragraph: str, banned: list[str]) -> tuple[str, int]:
    """Find the most common word in a paragraph excluding banned words.

    Time: O(n), Space: O(k) where k is unique words

    Args:
        paragraph: Input paragraph text
        banned: List of words to exclude from counting

    Returns:
        Tuple of (most_common_word, frequency)

    Examples:
        >>> most_common_word("Bob hit a ball, the hit BALL flew far after it was hit.", ["hit"])
        ('ball', 2)
        >>> most_common_word("a, a, a, a, b,b,b,c, c", ["a"])
        ('b', 3)
        >>> most_common_word("a.", [])
        ('a', 1)

    Raises:
        ValueError: If no valid words found after filtering banned words
    """
    # Convert to lowercase for case-insensitive processing
    text = paragraph.lower()

    # Extract words manually by splitting on non-alphabetic characters
    words = []
    current_word = ""

    for char in text:
        if char.isalpha():
            current_word += char
        else:
            if current_word:
                words.append(current_word)
                current_word = ""

    # Add the last word if exists
    if current_word:
        words.append(current_word)

    # Create banned words set for faster lookup
    banned_set = {word.lower() for word in banned}

    # Filter out banned words
    filtered_words = [word for word in words if word not in banned_set]

    if not filtered_words:
        raise ValueError("No valid words found after filtering banned words")

    # Count word frequencies manually
    word_count = {}
    for word in filtered_words:
        word_count[word] = word_count.get(word, 0) + 1

    # Find most common word manually
    most_common_word = ""
    max_count = 0

    for word, count in word_count.items():
        if count > max_count:
            max_count = count
            most_common_word = word

    return most_common_word, max_count


def most_common_word_v2(paragraph: str, banned: list[str]) -> tuple[str, int]:
    """Find the most common word in a paragraph excluding banned words."""
    # Convert to lowercase and extract words using regex
    # words = re.findall(r'\b[a-zA-Z]+\b', paragraph.lower())
    words = re.findall(r"\b\w+\b", paragraph.lower())

    # Filter out banned words
    banned_set = {word.lower() for word in banned}
    filtered_words = [word for word in words if word not in banned_set]

    if not filtered_words:
        raise ValueError("No valid words found after filtering banned words")

    # Count word frequencies
    word_count = Counter(filtered_words)
    print(f"Word counts: {word_count}")

    # Get most common word
    most_common = word_count.most_common(1)[0]
    return most_common[0], most_common[1]


def main():
    """Main function for manual testing."""
    with PerformanceTimer("common_word_v1", logger):
        most_common = most_common_word_v1("Bob hit a ball, the hit BALL, up2date flew far after it was hit.", ["hit"])
    print(f"Most common word: {most_common}")

    with PerformanceTimer("common_word_v2", logger):
        most_common = most_common_word_v2("Bob hit a ball, the hit BALL, up2date flew far after it was hit.", ["HIT"])
    print(f"Most common word: {most_common}")


if __name__ == "__main__":
    main()
