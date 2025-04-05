from query_faiss import faiss_search
import numpy as np
from rapidfuzz import fuzz

# Test queries with expected relevant test names (adjust names as per your CSV)
test_queries = {
    "Looking for Java developers who understand design patterns": [
        "Java Design Patterns (New)", "Core Java (Advanced Level) (New)", "Java Frameworks (New)"
    ],
    "Need an assessment for a software analyst role": [
        "Software Business Analysis"
    ],
    "Hiring fresh graduates for a tech role": [
        "Graduate + 8.0 Job Focused Assessment", "Graduate 8.0 Job Focused Assessment"
    ],
    "Seeking data scientists with ML knowledge": [
        "Data Science (New)", "IBM DataStage (New)"
    ]
}


def is_relevant(retrieved, relevant_list, threshold=85):
    return any(fuzz.partial_ratio(retrieved, rel) >= threshold for rel in relevant_list)

def precision_at_k(relevant, retrieved, k):
    retrieved_at_k = retrieved[:k]
    relevant_count = sum(is_relevant(r, relevant) for r in retrieved_at_k)
    return relevant_count / k

def recall_at_k(relevant, retrieved, k):
    retrieved_at_k = retrieved[:k]
    matched_relevant = sum(is_relevant(r, relevant) for r in retrieved_at_k)
    return matched_relevant / len(relevant) if relevant else 0.0

def mrr(relevant, retrieved):
    for idx, item in enumerate(retrieved):
        if is_relevant(item, relevant):
            return 1 / (idx + 1)
    return 0.0

precisions, recalls, mrrs = [], [], []

for query, relevant_tests in test_queries.items():
    results = faiss_search(query)
    retrieved_tests = results['Test Name'].tolist()

    print(f"\n🔎 Query: {query}")
    print("📄 Retrieved:", retrieved_tests)

    p5 = precision_at_k(relevant_tests, retrieved_tests, 5)
    r5 = recall_at_k(relevant_tests, retrieved_tests, 5)
    mrr_score = mrr(relevant_tests, retrieved_tests)

    print(f"📌 Precision@5: {p5:.2f}")
    print(f"📌 Recall@5: {r5:.2f}")
    print(f"📌 MRR: {mrr_score:.2f}")

    precisions.append(p5)
    recalls.append(r5)
    mrrs.append(mrr_score)

print("\n=== 📊 Overall Evaluation ===")
print(f"✅ Mean Precision@5: {np.mean(precisions):.2f}")
print(f"✅ Mean Recall@5: {np.mean(recalls):.2f}")
print(f"✅ Mean MRR: {np.mean(mrrs):.2f}")
