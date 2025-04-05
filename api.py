from fastapi import FastAPI
from pydantic import BaseModel
import pandas as pd
from query_faiss import faiss_search  # ✅ Use your existing logic

app = FastAPI()

# Define input schema
class QueryInput(BaseModel):
    query: str
    top_k: int = 6  # Optional override

@app.post("/recommend")
async def recommend(query_input: QueryInput):
    # Run your intelligent search
    results = faiss_search(query_input.query, top_k=query_input.top_k)

    # Prepare output
    recs = results[["Test Name", "Remote Testing", "Adaptive/IRT", "Duration", "Test Type", "Link"]].to_dict(orient="records")
    return {
        "query": query_input.query,
        "recommendations": recs
    }
