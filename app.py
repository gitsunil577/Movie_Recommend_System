import pickle
import streamlit as st
import requests
import pandas as pd
import numpy as np
from dotenv import load_dotenv
import time
import os

load_dotenv()

# ✅ Install missing dependencies (Optional)
try:
    from requests_cache import CachedSession
except ImportError:
    os.system("pip install requests-cache")
    from requests_cache import CachedSession

# ✅ Configure API Caching (Reduces API Calls & Prevents Rate Limiting)
session = CachedSession("movie_cache", backend="sqlite", expire_after=60 * 60 * 24)  # 24-hour cache


# ✅ Fetch Movie Poster with Error Handling
def fetch_poster(movie_id):
    API = os.environ['API_KEY']
    url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key={API}&language=en-US"

    try:
        response = session.get(url, timeout=10)
        response.raise_for_status()  # Ensure HTTP request was successful
        data = response.json()

        if "poster_path" in data and data["poster_path"]:
            return f"https://image.tmdb.org/t/p/w500/{data['poster_path']}"

        st.warning(f"⚠️ No poster found for Movie ID: {movie_id}")

    except requests.exceptions.HTTPError as http_err:
        st.error(f"HTTP Error: {http_err}")
    except requests.exceptions.RequestException as req_err:
        st.error(f"Request Error: {req_err}")

    return "https://via.placeholder.com/150"

# ✅ Load Movie Data
try:
    movies = pickle.load(open("model/movie_list.pkl", "rb"))
    similarity = pickle.load(open("model/similarity.pkl", "rb"))

    if not isinstance(movies, pd.DataFrame):
        st.error("⚠️ The loaded movie data is not in the expected format (DataFrame).")
        st.stop()
    
    if "movie_id" not in movies.columns:
        st.error("⚠️ 'movie_id' column is missing in the dataset.")
        st.stop()
    
    if not isinstance(similarity, (np.ndarray, list, pd.DataFrame)):
        st.error("⚠️ The loaded similarity matrix is not in the expected format.")
        st.stop()

except FileNotFoundError:
    st.error("⚠️ Model files not found. Ensure 'movie_list.pkl' and 'similarity.pkl' exist.")
    st.stop()
except Exception as e:
    st.error(f"⚠️ Error loading model files: {e}")
    st.stop()

# ✅ Movie Recommendation Function (Fixed `movie` issue)
def recommend(movie):
    """Returns a list of recommended movie names & posters."""
    if movie not in movies["title"].values:
        return [], []

    index = movies[movies["title"] == movie].index[0]
    distances = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])

    recommended_movie_names = []
    recommended_movie_posters = []

    for i in distances[1:6]:  # Top 5 recommendations
        movie_id = movies.iloc[i[0]].movie_id

        # Debugging: Check if movie_id exists
        if pd.isna(movie_id):
            st.warning(f"⚠️ Missing movie_id for {movies.iloc[i[0]].title}. Skipping...")
            continue

        recommended_movie_posters.append(fetch_poster(movie_id))
        recommended_movie_names.append(movies.iloc[i[0]].title)

    return recommended_movie_names, recommended_movie_posters

# ✅ Streamlit UI
st.header("🎬 Movie Recommender System")

# Dropdown for movie selection
selected_movie = st.selectbox("Type or select a movie from the dropdown", movies["title"].values)

# Show recommendations on button click
if st.button("Show Recommendation"):
    recommended_movie_names, recommended_movie_posters = recommend(selected_movie)

    if not recommended_movie_names:
        st.warning("⚠️ No recommendations found. Please try another movie.")
    else:
        cols = st.columns(len(recommended_movie_names))  # Dynamically create columns

        for idx, col in enumerate(cols):
            with col:
                st.text(recommended_movie_names[idx])
                st.image(recommended_movie_posters[idx])
