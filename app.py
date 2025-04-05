# import streamlit as st
# import faiss
# import pickle
# import numpy as np
# import pandas as pd
# from sentence_transformers import SentenceTransformer

# # Load FAISS index
# with open("embed/faiss_index.pkl", "rb") as f:
#     index, df = pickle.load(f)

# # Load embedding model
# model = SentenceTransformer("all-MiniLM-L6-v2")

# # Streamlit App Title
# st.title("🔍 SHL Assessment Recommendation Engine")

# # Description
# st.write("Enter a job description or role to get matching SHL assessments.")

# # Search box
# query = st.text_input("💼 Enter job description or query:")

# # Handle search
# if query:
#     with st.spinner("Searching..."):
#         query_vec = model.encode([query]).astype('float32')
#         distances, indices = index.search(query_vec, 10)
#         results = df.iloc[indices[0]].copy()

#         # Create clickable links for "Test Name"
#         results["Test Name"] = results.apply(
#             lambda row: f"[{row['Test Name']}]({row['Link']})", axis=1
#         )

#         # Select and rename columns
#         results = results[["Test Name", "Remote Testing", "Adaptive/IRT", "Test Type", "Duration"]]
#         results.columns = ["Assessment Name", "Remote", "Adaptive/IRT", "Test Type", "Duration"]

#         st.success("Top matching assessments:")
#         st.write(results.to_markdown(index=False), unsafe_allow_html=True)
import streamlit as st
import pandas as pd
from query_faiss import faiss_search  # ✅ Import your search logic

# Streamlit App Title
st.title("🔍 SHL Assessment Recommendation Engine")

# Description
st.write("Enter a job description or role to get matching SHL assessments.")

# Search box
query = st.text_input("💼 Enter job description or query:")

# Handle search
if query:
    with st.spinner("Searching..."):
        results = faiss_search(query)

        # Create clickable links
        results["Assessment Name"] = results.apply(
            lambda row: f"[{row['Test Name']}]({row['Link']})", axis=1
        )

        # Select and rename columns
        results = results[["Assessment Name", "Remote Testing", "Adaptive/IRT", "Test Type", "Duration"]]
        results.columns = ["Assessment Name", "Remote", "Adaptive/IRT", "Test Type", "Duration"]

        st.success("Top matching assessments:")
        st.write(results.to_markdown(index=False), unsafe_allow_html=True)
