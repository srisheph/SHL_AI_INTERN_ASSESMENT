import os
import pandas as pd
import numpy as np
import faiss
import pickle
from tqdm import tqdm
from sentence_transformers import SentenceTransformer

# Paths (✅ relative and clean)
DATA_PATH = os.path.join("data", "final_tests.csv")
INDEX_PATH = os.path.join("embed", "faiss_index.pkl")

# Load data
df = pd.read_csv(DATA_PATH)

# Prepare full_text for embedding
df['full_text'] = (
    "Test Name: " + df['Test Name'] + "\n" +
    "Test Type: " + df['Test Type'] + "\n" +
    "Remote Testing: " + df['Remote Testing'].astype(str) + "\n" +
    "Adaptive/IRT: " + df['Adaptive/IRT'].astype(str) + "\n" +
    "Duration: " + df['Duration'].astype(str) + "\n" +
    "Link: " + df['Link']
)

# Load embedding model
model = SentenceTransformer('all-MiniLM-L6-v2')

# Generate embeddings
print("⚙️ Generating embeddings...")
embeddings = model.encode(df['full_text'].tolist(), show_progress_bar=True)
embedding_matrix = np.array(embeddings).astype('float32')

# Create FAISS index
index = faiss.IndexFlatL2(embedding_matrix.shape[1])
index.add(embedding_matrix)

# Save index and dataframe
os.makedirs("embed", exist_ok=True)
with open(INDEX_PATH, 'wb') as f:
    pickle.dump((index, df), f)

print("✅ Embedding complete and FAISS index saved at:", INDEX_PATH)
