import pandas as pd
import numpy as np
import faiss
import pickle
from tqdm import tqdm
from sentence_transformers import SentenceTransformer

# Load data
df = pd.read_csv(r'C:/Users/acer/OneDrive/Desktop/shl_assesment/data/final_tests.csv')

# Prepare full_text for embedding (✅ fixed \n issue)
df['full_text'] = (
    "Test Name: " + df['Test Name'] + "\n" +
    "Test Type: " + df['Test Type'] + "\n" +
    "Remote Testing: " + df['Remote Testing'].astype(str) + "\n" +
    "Adaptive/IRT: " + df['Adaptive/IRT'].astype(str) + "\n" +
    "Duration: " + df['Duration'].astype(str) + "\n" +
    "Link: " + df['Link']
)

# Load local embedding model
model = SentenceTransformer('all-MiniLM-L6-v2')

# Generate embeddings
print("Generating embeddings...")
embeddings = model.encode(df['full_text'].tolist(), show_progress_bar=True)

# Convert to float32 numpy array
embedding_matrix = np.array(embeddings).astype('float32')

# Create FAISS index (FlatL2 for cosine similarity-like search)
index = faiss.IndexFlatL2(embedding_matrix.shape[1])
index.add(embedding_matrix)

# Save the index + dataframe
with open('C:/Users/acer/OneDrive/Desktop/shl_assesment/embed/faiss_index.pkl', 'wb') as f:
    pickle.dump((index, df), f)

print("✅ Embedding complete and FAISS index saved.")
