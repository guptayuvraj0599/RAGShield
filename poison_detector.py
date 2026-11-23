
import re


# Words that are too common to be useful for comparing documents.
STOP_WORDS = {
    "the", "is", "are", "was", "were", "a", "an", "and",
    "or", "to", "of", "in", "on", "for", "with", "from",
    "by", "at", "as", "it", "this", "that", "be", "should",
    "can", "may", "must", "not", "their", "they", "students",
    "university"
}


SUSPICIOUS_PHRASES = [
    "unverified notice",
    "not verified",
    "ignore official",
    "do not rely on official",
    "unofficial student groups",
    "bypass verification",
    "disregard previous information",
    "ignore previous instructions",
    "override official information"
]


MANIPULATIVE_PHRASES = [
    "do not check",
    "should not rely",
    "ignore official",
    "bypass verification",
    "disregard previous information",
    "ignore previous instructions",
    "override official information"
]


def tokenize(text):
    words = re.findall(r"\b[a-z0-9]+\b", text.lower())

    return {
        word for word in words
        if word not in STOP_WORDS and len(word) > 2
    }


def find_conflicts(document_text, trusted_documents):
    """
    Identify possible numerical conflicts with trusted documents.

    This is a heuristic, not a complete natural-language
    contradiction detector.
    """

    document_words = tokenize(document_text)
    document_numbers = set(
        re.findall(r"\b\d+(?:\.\d+)?\b", document_text)
    )

    conflicts = []

    if not document_numbers:
        return conflicts

    for trusted_doc in trusted_documents:
        trusted_text = trusted_doc["text"]

        trusted_words = tokenize(trusted_text)
        trusted_numbers = set(
            re.findall(r"\b\d+(?:\.\d+)?\b", trusted_text)
        )

        if not trusted_numbers:
            continue

        common_words = document_words.intersection(trusted_words)

        if len(common_words) < 2:
            continue

        overlap = len(common_words) / max(
            1, len(document_words.union(trusted_words))
        )

        if overlap >= 0.12 and document_numbers.isdisjoint(
            trusted_numbers
        ):
            conflicts.append({
                "trusted_source": trusted_doc.get("source", "unknown"),
                "overlapping_terms": sorted(common_words),
                "document_numbers": sorted(document_numbers),
                "trusted_numbers": sorted(trusted_numbers)
            })

    return conflicts


def detect_poison(document, trusted_sources, trusted_documents):
    """
    Rule-based suspicious document detection.

    IMPORTANT:
    This function does not access the is_poisoned label.
    """

    text = document["text"].lower()
    source = document.get("source", "unknown")

    score = 0
    reasons = []

    # Rule 1: Source reliability
    if source not in trusted_sources:
        score += 35
        reasons.append("Source is not in the trusted source list.")

    # Rule 2: Suspicious language
    matched_phrases = [
        phrase for phrase in SUSPICIOUS_PHRASES
        if phrase in text
    ]

    if matched_phrases:
        score += min(30, 15 * len(matched_phrases))
        reasons.append(
            "Suspicious phrases found: "
            + ", ".join(matched_phrases)
        )

    # Rule 3: Manipulative instructions
    matched_instructions = [
        phrase for phrase in MANIPULATIVE_PHRASES
        if phrase in text
    ]

    if matched_instructions:
        score += min(20, 10 * len(matched_instructions))
        reasons.append(
            "Potentially manipulative language detected: "
            + ", ".join(matched_instructions)
        )

    # Rule 4: Numerical conflicts with trusted documents
    conflicts = find_conflicts(text, trusted_documents)

    if conflicts:
        score += 35
        reasons.append(
            f"Potential numerical conflict with "
            f"{len(conflicts)} trusted document(s)."
        )

    score = min(score, 100)

    if score >= 60:
        risk_level = "HIGH"
        decision = "BLOCK"
    elif score >= 30:
        risk_level = "MEDIUM"
        decision = "REVIEW"
    else:
        risk_level = "LOW"
        decision = "ALLOW"

    return {
        "risk_score": score,
        "risk_level": risk_level,
        "decision": decision,
        "reasons": reasons,
        "conflicts": conflicts
    }