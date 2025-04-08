from fastapi import FastAPI
from pydantic import BaseModel
import pandas as pd
from query_faiss import faiss_search
import uvicorn

app = FastAPI()

# Define input schema
class QueryInput(BaseModel):
    query: str
    top_k: int = 6  # Optional override

@app.post("/recommend")
async def recommend(query_input: QueryInput):
    # Run FAISS search
    results = faiss_search(query_input.query, top_k=query_input.top_k)

    # Select relevant columns
    recs = results[["Test Name", "Remote Testing", "Adaptive/IRT", "Duration", "Test Type", "Link"]].copy()

    # Fix boolean columns to Yes/No strings
    recs["Remote Testing"] = recs["Remote Testing"].apply(lambda x: "Yes" if x else "No")
    recs["Adaptive/IRT"] = recs["Adaptive/IRT"].apply(lambda x: "Yes" if x else "No")
    recs["Duration"] = recs["Duration"].apply(lambda x: int(x) if pd.notnull(x) else 0)

    # Rename keys to match required JSON
    recs.rename(columns={
        "Test Name": "test_name",
        "Remote Testing": "remote_support",
        "Adaptive/IRT": "adaptive_support",
        "Duration": "duration",
        "Test Type": "test_type",
        "Link": "url"
    }, inplace=True)

    # Return final JSON
    return {
        "query": query_input.query,
        "recommended_assessments": recs.to_dict(orient="records")
    }
