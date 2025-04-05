# SHL_AI_INTERN_ASSESMENT
# SHL Assessment Recommendation Engine 🧠✨

This Streamlit-based web application recommends relevant SHL assessments based on a user's job role or natural language job description using semantic search powered by FAISS and Sentence Transformers.

---

## 🚀 Features

- 🔍 Semantic search using FAISS and Sentence Transformers
- 🤖 Intelligent test mapping from natural language queries
- 📊 Recommends top N suitable SHL assessments
- 🌐 Deployed with Streamlit Cloud

---

## 💡 Problem Statement

SHL offers a variety of tests for different job roles. However, selecting the most suitable assessment for a specific job profile or description can be a challenge. This tool solves that by intelligently matching a user's query to the right assessments.

---

## 🧠 Approach

### 1. **Data Collection**
- Scraped SHL's product catalog (Repackaged + Core tests) using Selenium
- Stored in `final_tests.csv` with fields: Test Name, Duration, Remote, Type, Link, etc.

### 2. **Embedding and Indexing**
- Converted job role/test names to sentence embeddings using `sentence-transformers`
- Built a FAISS index for fast similarity search

### 3. **Query Handling**
- User inputs a job role or job description
- It is converted to an embedding and matched against indexed embeddings
- Top-k matches are retrieved and displayed with relevant metadata

---

## 📁 Project Structure
├── app.py # Streamlit web app 

├──data/final_tests.csv # Product catalog with test metadata 

├── embed/faiss_index.pkl # Serialized FAISS index 

├── requirements.txt # Required Python packages 

└── README.md # Project documentation

## ⚙️ Setup Instructions

git clone https://github.com/your-username/shl-assessment-app.git

cd shl-assessment-app

pip install -r requirements.txt

streamlit run app.py

📦 Dependencies
streamlit

pandas

sentence-transformers

faiss-cpu

scikit-learn

🧪 Example Queries
Try these in the input field:

"Looking for an assessment for a software engineer"

"I need a test for hiring a retail store manager"

"Aptitude test for business analysts"

👩‍💻 Author

Shephali Srivastava

[GitHub](https://github.com/srisheph)
 | [LinkedIn](https://www.linkedin.com/in/srisheph/)
 

Here's a screenshot of the code working:

![Screenshot 2025-04-05 144956](https://github.com/user-attachments/assets/e248babe-295b-478f-b943-b3b9b64c447a)



🌐 Live App
Click here to view the deployed app 🚀

Link







