import pandas as pd
import streamlit as st
import pickle
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
import requests
import os
from dotenv import load_dotenv
load_dotenv()
my_api_key = os.getenv("API_KEY")

# print(my_api_key)

vector = pickle.load(open('vector.pkl', 'rb'))
similarity_list = cosine_similarity(vector)
movie_dict = pickle.load(open('movie_list_dict.pkl', 'rb'))
movie_list = pickle.load(open('movie_list.pkl', 'rb'))
movies_list = pd.DataFrame(movie_dict)
st.title('Movie Recommendation System')

import requests
import time

# Create ONE session globally
session = requests.Session()

def fetch_poster(movie_id):
    url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key={my_api_key}"

    # Retry up to 3 times
    for attempt in range(3):
        try:
            response = session.get(url, timeout=10)

            # Raise exception for 4xx/5xx responses
            response.raise_for_status()

            data = response.json()

            poster_path = data.get("poster_path")

            if poster_path:
                return f"https://image.tmdb.org/t/p/w500{poster_path}"

            return "https://via.placeholder.com/500x750?text=No+Poster"

        except requests.exceptions.RequestException as e:
            st.warning(
                f"Please wait while we load the recommendations, Attempt {attempt + 1}/3 failed for movie {movie_id} : {e}"
            )

            # Wait before retrying
            time.sleep(1)

    # If all retries fail
    return "https://via.placeholder.com/500x750?text=Error"


def recommend(movie):
    index = movies_list[movies_list['title'] == movie].index[0]
    # st.write(index)
    distances = sorted(list(enumerate(similarity_list[index])),reverse=True,key = lambda x: x[1])
    recommended_movies = []
    recommended_movies_posters = []
    for i in distances[1:6]:
        movie_id = movies_list.iloc[i[0]].movie_id
        recommended_movies.append(movies_list.iloc[i[0]].title)
        # fetch poster from API call
        recommended_movies_posters.append(fetch_poster(movie_id))

    return recommended_movies,recommended_movies_posters


selected_movie_name = st.selectbox('Select to movie to get movie recommendation',movies_list['title'].values)

if st.button('Show Recommendation'):
    recommended_movie_names,recommended_movie_posters = recommend(selected_movie_name)
    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        st.text(recommended_movie_names[0])
        st.image(recommended_movie_posters[0])
    with col2:
        st.text(recommended_movie_names[1])
        st.image(recommended_movie_posters[1])

    with col3:
        st.text(recommended_movie_names[2])
        st.image(recommended_movie_posters[2])
    with col4:
        st.text(recommended_movie_names[3])
        st.image(recommended_movie_posters[3])
    with col5:
        st.text(recommended_movie_names[4])
        st.image(recommended_movie_posters[4])


