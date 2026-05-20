import re
from dataclasses import asdict, dataclass


POSITIVE_WORDS = {
    "growth", "secure", "success", "improve", "efficient", "positive", "profit",
    "innovation", "strong", "benefit", "opportunity", "support",
}
NEGATIVE_WORDS = {
    "risk", "loss", "delay", "decline", "weak", "negative", "problem",
    "failure", "threat", "uncertain", "concern", "crisis",
}
PRONOUNS = {"i", "we", "my", "ours", "us"}


@dataclass
class TextMetrics:
    word_count: int
    sentence_count: int
    polarity: float
    subjectivity: float
    fog_index: float
    avg_sentence_length: float
    complex_word_count: int
    personal_pronouns: int

    def to_dict(self) -> dict:
        return asdict(self)


def words(text: str) -> list[str]:
    return re.findall(r"[A-Za-z]+", text.lower())


def sentence_count(text: str) -> int:
    return max(1, len(re.findall(r"[.!?]+", text)))


def syllable_count(word: str) -> int:
    groups = re.findall(r"[aeiouy]+", word.lower())
    count = len(groups)
    if word.endswith("e") and count > 1:
        count -= 1
    return max(1, count)


def analyze_text(text: str) -> TextMetrics:
    tokens = words(text)
    total_words = max(1, len(tokens))
    sentences = sentence_count(text)
    positive = sum(token in POSITIVE_WORDS for token in tokens)
    negative = sum(token in NEGATIVE_WORDS for token in tokens)
    subjective = positive + negative
    complex_words = sum(syllable_count(token) >= 3 for token in tokens)
    avg_sentence = total_words / sentences
    complex_pct = complex_words / total_words * 100
    fog = 0.4 * (avg_sentence + complex_pct)
    polarity = (positive - negative) / max(1, subjective)
    subjectivity = subjective / total_words
    pronouns = sum(token in PRONOUNS for token in tokens)
    return TextMetrics(
        word_count=total_words,
        sentence_count=sentences,
        polarity=round(polarity, 4),
        subjectivity=round(subjectivity, 4),
        fog_index=round(fog, 2),
        avg_sentence_length=round(avg_sentence, 2),
        complex_word_count=complex_words,
        personal_pronouns=pronouns,
    )
