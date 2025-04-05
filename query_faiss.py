# import pickle
# import faiss
# import re
# import pandas as pd
# from sentence_transformers import SentenceTransformer, util
# from sklearn.feature_extraction.text import TfidfVectorizer

# # Load FAISS index and DataFrame
# with open('embed/faiss_index.pkl', 'rb') as f:
#     index, df = pickle.load(f)

# # Load embedding model
# model = SentenceTransformer('all-MiniLM-L6-v2')

# # Duration extractor
# def extract_duration(text):
#     match = re.search(r'(\d+)\s*(minutes|min)', text.lower())
#     if match:
#         return int(match.group(1))
#     return None

# # Query Expansion using synonyms (basic version)
# def expand_query(query):
#     additions = {
#         'developer': ['programmer', 'engineer', 'coder'],
#         'analyst': ['examiner', 'evaluator'],
#         'graduate': ['fresher', 'entry-level'],
#         'hiring': ['recruiting', 'looking for'],
#     }
#     expanded = [query]
#     for word, synonyms in additions.items():
#         if word in query.lower():
#             for s in synonyms:
#                 expanded.append(query.lower().replace(word, s))
#     return list(set(expanded))

# # Keyword Overlap Score
# def keyword_score(query, text):
#     q_words = set(re.findall(r'\b\w+\b', query.lower()))
#     t_words = set(re.findall(r'\b\w+\b', text.lower()))
#     return len(q_words & t_words) / (len(q_words) + 1e-5)

# # Filter and Re-rank
# def filter_results(df_results, query, query_embedding):
#     query_lower = query.lower()
#     desired_duration = extract_duration(query_lower)

#     def match_duration(row):
#         dur = extract_duration(str(row.get("Duration", "")))
#         if dur is not None and desired_duration is not None:
#             return abs(dur - desired_duration) <= 10
#         return True

#     df_results = df_results[df_results.apply(match_duration, axis=1)]

#     # Add hybrid score: FAISS + keyword overlap
#     df_results['keyword_score'] = df_results.apply(
#         lambda row: keyword_score(query, ' '.join(str(val) for val in row.values)), axis=1
#     )

#     row_embeddings = model.encode(df_results['Test Name'].tolist(), convert_to_tensor=True)
#     query_tensor = model.encode(query, convert_to_tensor=True)
#     df_results['semantic_score'] = util.pytorch_cos_sim(query_tensor, row_embeddings)[0].tolist()

#     df_results['hybrid_score'] = df_results['semantic_score'] + 0.3 * df_results['keyword_score']
#     df_sorted = df_results.sort_values(by='hybrid_score', ascending=False)

#     return df_sorted.head(6) if not df_sorted.empty else df_results.head(6)

# # 🔍 Main function to use in evaluate.py
# def faiss_search(query, top_k=12):
#     expanded_queries = expand_query(query)
#     query_embedding = model.encode([' '.join(expanded_queries)]).astype('float32')
#     distances, indices = index.search(query_embedding, top_k)
#     results = df.iloc[indices[0]].copy()
#     results['Score'] = distances[0]
#     return filter_results(results, query, query_embedding)

# # Manual test
# if __name__ == "__main__":
#     query = input("Enter job description or query: ")
#     top_results = faiss_search(query)
#     print(top_results[['Test Name', 'Remote Testing', 'Adaptive/IRT', 'Duration', 'Test Type', 'Link']])


import pickle
import faiss
import re
import pandas as pd
from sentence_transformers import SentenceTransformer, util
from sklearn.feature_extraction.text import TfidfVectorizer
import numpy as np

# Load FAISS index and DataFrame
with open('embed/faiss_index.pkl', 'rb') as f:
    index, df = pickle.load(f)

# Load embedding model
model = SentenceTransformer('all-MiniLM-L6-v2')

# Duration extractor
def extract_duration(text):
    match = re.search(r'(\d+)\s*(minutes|min)', text.lower())
    if match:
        return int(match.group(1))
    return None

# Query Expansion
def expand_query(query):
    additions = {
        'developer': ['programmer', 'engineer', 'coder'],
        'analyst': ['examiner', 'evaluator'],
        'graduate': ['fresher', 'entry-level'],
        'hiring': ['recruiting', 'looking for'],
    }
    expanded = [query]
    for word, synonyms in additions.items():
        if word in query.lower():
            for s in synonyms:
                expanded.append(query.lower().replace(word, s))
    return list(set(expanded))

# Keyword Overlap Score
def keyword_score(query, text):
    q_words = set(re.findall(r'\b\w+\b', query.lower()))
    t_words = set(re.findall(r'\b\w+\b', text.lower()))
    return len(q_words & t_words) / (len(q_words) + 1e-5)

# Filter and Re-rank
def filter_results(df_results, query, query_embedding):
    query_lower = query.lower()
    desired_duration = extract_duration(query_lower)

    def match_duration(row):
        dur = extract_duration(str(row.get("Duration", "")))
        if dur is not None and desired_duration is not None:
            return abs(dur - desired_duration) <= 10
        return True

    df_results = df_results[df_results.apply(match_duration, axis=1)].copy()

    # Add hybrid score
    df_results['keyword_score'] = df_results.apply(
        lambda row: keyword_score(query, ' '.join(str(val) for val in row.values)), axis=1
    )

    row_embeddings = model.encode(df_results['Test Name'].tolist(), convert_to_tensor=True)
    query_tensor = model.encode(query, convert_to_tensor=True)
    df_results['semantic_score'] = util.pytorch_cos_sim(query_tensor, row_embeddings)[0].cpu().numpy().tolist()

    df_results['hybrid_score'] = df_results['semantic_score'] + 0.3 * df_results['keyword_score']
    df_sorted = df_results.sort_values(by='hybrid_score', ascending=False)

    return df_sorted.head(6) if not df_sorted.empty else df_results.head(6)

# 🔍 Main function to use in API
def faiss_search(query, top_k=12):
    expanded_queries = expand_query(query)
    query_embedding = model.encode([' '.join(expanded_queries)]).astype('float32')
    distances, indices = index.search(query_embedding, top_k)
    results = df.iloc[indices[0]].copy()
    results['Score'] = distances[0]
    return filter_results(results, query, query_embedding)

# Test (optional)
if __name__ == "__main__":
    query = input("Enter job description or query: ")
    top_results = faiss_search(query)
    print(top_results[['Test Name', 'Remote Testing', 'Adaptive/IRT', 'Duration', 'Test Type', 'Link']])
