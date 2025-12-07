# Movie Recommender System

A content-based movie recommender system that suggests movies similar to a user's selection. This project uses the TMDB dataset and is built with Python and Streamlit.

## 🚀 Features

-   **Movie Recommendations:** Get a list of 5 movies similar to your selection.
-   **Movie Posters:** Displays movie posters for a visually appealing experience.
-   **Simple Interface:** Easy-to-use interface built with Streamlit.

## 🛠️ Tech Stack

-   **Python:** The core programming language.
-   **Streamlit:** For creating the web application.
-   **Pandas & NumPy:** For data manipulation and numerical operations.
-   **Scikit-learn:** Used for calculating cosine similarity (implicitly via the `similarity.pkl` file).
-   **TMDB API:** To fetch movie posters and details.
-   **Requests & Requests-Cache:** For making API requests and caching the responses.

## 📂 Project Structure

```
.
├── app.py                  # Main Streamlit application
├── model/
│   ├── movie_list.pkl      # Pickled Pandas DataFrame of movies
│   └── similarity.pkl      # Pickled similarity matrix
├── movie_cache.sqlite      # SQLite database for API response caching
└── README.md               # This file
```

## ⚙️ Setup and Installation

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/your-username/movie-recommender-system-tmdb-dataset.git
    cd movie-recommender-system-tmdb-dataset
    ```

2.  **Install dependencies:**
    Make sure you have Python installed. Then, install the required libraries:
    ```bash
    pip install streamlit requests pandas numpy requests-cache
    ```

3.  **Get a TMDB API Key:**
    -   Create an account on [The Movie Database (TMDB)](https://www.themoviedb.org/).
    -   Go to your account settings, then the "API" section to get your API key.
    -   Open `app.py` and replace `"393fbfba600f6060813762a396dbd7d4"` in the `fetch_poster` function with your API key.

## ▶️ How to Run

1.  Open your terminal in the project directory.
2.  Run the following command:
    ```bash
    streamlit run app.py
    ```
3.  Ensure your internet is connected via VPN for API support (if required by your network configuration).
4.  The application will open in your web browser.

## 📖 How It Works

The recommender system is content-based. It uses a pre-computed similarity matrix (`similarity.pkl`) to find movies that are similar to the one you select. The similarity is likely based on movie attributes like genre, keywords, cast, and crew from the TMDB dataset.

When you select a movie, the application:
1.  Finds the movie in the `movie_list.pkl` dataset.
2.  Gets the similarity scores for that movie from the `similarity.pkl` matrix.
3.  Sorts the movies based on their similarity scores.
4.  Recommends the top 5 most similar movies.
5.  Fetches the movie posters from the TMDB API to display them.

## 🙏 Acknowledgements

-   [The Movie Database (TMDB)](https://www.themoviedb.org/) for providing the dataset and API.
-   [Streamlit](https://streamlit.io/) for the awesome web framework.