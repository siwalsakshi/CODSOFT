import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# --- Step 1: Load sample dataset ---
movies = pd.DataFrame({
    "movie_id": [1, 2, 3, 4, 5],
    "title": ["Inception", "Interstellar", "The Dark Knight", "The Prestige", "Memento"],
    "genre": ["Sci-Fi Thriller", "Sci-Fi Adventure", "Action Crime", "Drama Mystery", "Thriller Mystery"]
})

ratings = pd.DataFrame({
    "user_id": [1,1,2,2,3,3,4,4,5],
    "movie_id": [1,2,2,3,3,4,4,5,1],
    "rating": [5,4,4,5,5,3,4,5,3]
})

# --- Step 2: Content-Based Similarity ---
vectorizer = TfidfVectorizer()
tfidf_matrix = vectorizer.fit_transform(movies['genre'])
cosine_sim = cosine_similarity(tfidf_matrix, tfidf_matrix)

# --- Step 3: Collaborative Filtering (User-Item Matrix) ---
user_item_matrix = ratings.pivot(index='user_id', columns='movie_id', values='rating').fillna(0)
user_sim = cosine_similarity(user_item_matrix)
user_sim_df = pd.DataFrame(user_sim, index=user_item_matrix.index, columns=user_item_matrix.index)

# --- Step 4: Hybrid Recommendation ---
def hybrid_recommend(user_id, liked_movie, top_n=3, alpha=0.5):
    """
    alpha = weight for content (0 to 1). 
    (1-alpha) = weight for collaborative filtering.
    """
    # Content-based part
    idx = movies[movies['title'] == liked_movie].index[0]
    sim_scores = list(enumerate(cosine_sim[idx]))
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
    sim_scores = sim_scores[1:top_n+1]
    content_recs = {movies.iloc[i[0]].movie_id: i[1] for i in sim_scores}
    
    # Collaborative part
    similar_users = user_sim_df[user_id].sort_values(ascending=False)[1:]
    top_user = similar_users.index[0]
    user_ratings = user_item_matrix.loc[user_id]
    top_user_ratings = user_item_matrix.loc[top_user]
    collab_recs = top_user_ratings[user_ratings == 0]
    collab_recs = collab_recs[collab_recs > 0].sort_values(ascending=False).to_dict()
    
    # Combine with weighted score
    final_scores = {}
    for m_id in set(content_recs.keys()).union(collab_recs.keys()):
        c_score = content_recs.get(m_id, 0)
        u_score = collab_recs.get(m_id, 0) / 5  # normalize rating to [0,1]
        final_scores[m_id] = alpha*c_score + (1-alpha)*u_score
    
    # Sort and return top N recommendations
    sorted_recs = sorted(final_scores.items(), key=lambda x: x[1], reverse=True)[:top_n]
    return [movies[movies['movie_id'] == m_id].title.values[0] for m_id, _ in sorted_recs]

# --- Example Usage ---
print("Hybrid recommendations for User 1 who liked 'Inception':")
print(hybrid_recommend(user_id=1, liked_movie="Inception", top_n=3, alpha=0.6))
