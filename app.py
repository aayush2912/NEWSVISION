from flask import Flask, request, jsonify
import pandas as pd
import numpy as np
from sentence_transformers import SentenceTransformer
from sklearn.neighbors import NearestNeighbors

print("Loading news dataset and BERT model...")
news_df = pd.read_csv("MIND_large_cleaned.csv")  
sbert_model = SentenceTransformer("all-MiniLM-L6-v2") 

print("Computing embeddings for news articles...")
news_df["title_vector"] = news_df["cleaned_title"].apply(lambda x: sbert_model.encode(x))
X_vectors = np.vstack(news_df["title_vector"].values)

print("Training Nearest Neighbors model for recommendations...")
knn = NearestNeighbors(n_neighbors=5, metric="cosine", algorithm="brute")
knn.fit(X_vectors)

# Create Flask App
app = Flask(__name__)

@app.route("/recommend", methods=["POST"])
def recommend_articles():
    try:
        data = request.get_json()
        user_input = data.get("title", "")

        if not user_input:
            return jsonify({"error": "No title provided"}), 400

        user_vector = sbert_model.encode(user_input).reshape(1, -1)

        distances, indices = knn.kneighbors(user_vector, n_neighbors=5)
        recommended_articles = news_df.iloc[indices.flatten()][["title", "category"]].to_dict(orient="records")

        return jsonify({"recommended_articles": recommended_articles})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
