import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# --- Step 1: Load MovieLens dataset ---
movies = pd.read_csv("/kaggle/input/recommendation-system-dataset/ml-latest-small/movies.csv")
ratings = pd.read_csv("/kaggle/input/recommendation-system-dataset/ml-latest-small/ratings.csv")

# --- Step 2: Content-Based Similarity (Genres) ---
vectorizer = TfidfVectorizer(stop_words='english')
tfidf_matrix = vectorizer.fit_transform(movies['genres'].fillna(''))
cosine_sim = cosine_similarity(tfidf_matrix, tfidf_matrix)

# --- Step 3: Collaborative Filtering (User-Item Matrix) ---
user_item_matrix = ratings.pivot(index='userId', columns='movieId', values='rating').fillna(0)
user_sim = cosine_similarity(user_item_matrix)
user_sim_df = pd.DataFrame(user_sim, index=user_item_matrix.index, columns=user_item_matrix.index)

# --- Step 4: Hybrid Recommendation ---
def hybrid_recommend(user_id, movie_index, top_n=5, alpha=0.5):
    idx = movie_index

    # --- content-based ---
    sim_scores = list(enumerate(cosine_sim[idx]))
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
    sim_scores = sim_scores[1:top_n+1]
    content_recs = {movies.iloc[i[0]].movieId: i[1] for i in sim_scores}

    # --- collaborative filtering ---
    if user_id not in user_item_matrix.index:
        return list(content_recs.keys())

    similar_users = user_sim_df[user_id].sort_values(ascending=False)[1:]
    top_user = similar_users.index[0]
    user_ratings = user_item_matrix.loc[user_id]
    top_user_ratings = user_item_matrix.loc[top_user]
    collab_recs = top_user_ratings[user_ratings == 0]
    collab_recs = collab_recs[collab_recs > 0].sort_values(ascending=False).to_dict()

    # --- combine ---
    final_scores = {}
    for m_id in set(content_recs.keys()).union(collab_recs.keys()):
        c_score = content_recs.get(m_id, 0)
        u_score = collab_recs.get(m_id, 0) / 5
        final_scores[m_id] = alpha*c_score + (1-alpha)*u_score

    sorted_recs = sorted(final_scores.items(), key=lambda x: x[1], reverse=True)[:top_n]
    return [movies[movies['movieId'] == m_id].title.values[0] for m_id, _ in sorted_recs]

# --- Step 5: Show options to user ---
def show_movie_options(n=10):
    print("\nAvailable Movies (sample):")
    sample_movies = movies.sample(n, random_state=None).reset_index(drop=True)
    for i, row in sample_movies.iterrows():
        print(f"{i+1}. {row['title']} ({row['genres']})")
    return sample_movies


# --- Main Interactive Loop ---
print("🎬 Welcome to the Hybrid Movie Recommendation System 🎬")

userid = int(input("Enter your User ID: "))

while True:
    sample_movies = show_movie_options(10)

    try:
        choice = int(input("\nEnter the number of the movie you like: "))
        liked_movie = sample_movies.iloc[choice-1]['title']
        movie_index = sample_movies.iloc[choice-1].name
    except (ValueError, IndexError):
        print("⚠️ Invalid choice! Please try again.")
        continue

    print(f"\n🎬 Hybrid recommendations for User {user_id} who liked '{liked_movie}':")
    for rec in hybrid_recommend(user_id=user_id, movie_index=movie_index, top_n=5, alpha=0.6):
        print(f"- {rec}")

    again = input("\nDo you want another recommendation? (y/n): ").strip().lower()
    if again != 'y':
        print("\n✅ Thank you for using our Movie Recommendation System! 🙌")
        break
