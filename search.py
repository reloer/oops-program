
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

from core.database import get_memories


def search_memories(query, top_k=5):
    memories = get_memories()

    if not memories:
        return []

    documents = [
        memory["title"] + " " +
        memory["content"] + " " +
        memory["category"] + " " +
        memory["tags"]
        for memory in memories
    ]

    documents.append(query)

    vectorizer = TfidfVectorizer(
        stop_words="english",
        ngram_range=(1, 2),
        max_features=30000
    )

    matrix = vectorizer.fit_transform(documents)

    scores = cosine_similarity(
        matrix[-1],
        matrix[:-1]
    ).flatten()

    ranked_indices = scores.argsort()[::-1]

    results = []

    for index in ranked_indices[:top_k]:
        if scores[index] > 0:
            memory = memories[index].copy()
            memory["score"] = float(scores[index])
            results.append(memory)

    return results
