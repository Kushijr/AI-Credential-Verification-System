def detect_fraud(text):

    text = text.lower()

    fake_keywords = [
        "fake",
        "invalid",
        "dummy",
        "sample",
        "test certificate",
        "not valid",
        "unauthorized",
        "forged"
    ]

    for word in fake_keywords:

        if word in text:

            return True

    # REQUIRED CERTIFICATE WORDS
    valid_keywords = [
        "certificate",
        "university",
        "student",
        "course",
        "completion"
    ]

    score = 0

    for word in valid_keywords:

        if word in text:

            score += 1

    # If too few valid words found -> reject
    if score < 2:

        return True

    return False