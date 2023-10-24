import streamlit as st
import pickle
import pandas as pd
import numpy as np
import requests
similarity = pickle.load(open('similarity.pkl','rb'))
movies_dic = pickle.load(open('movies_dic.pkl','rb'))
movies = pd.DataFrame(movies_dic)

def fetch_poster(movie_id):
    base_url = "https://api.themoviedb.org/3/movie/{}?language=en-US"
    api_url = base_url.format(movie_id)
    bearer_token = "eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiJhYzhkZTI3NGUyNDU3MmQxMzhlMzgyYTEwYmQ1ZjQ0YiIsInN1YiI6IjY1MzI1ZDExOGQyMmZjMDEwYjcxZGVlYSIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ.zut1ltjaMBy7C4yP0kwZcTYcJ7xHFqIrd44no6BfvRY"
    headers = {
    "Authorization": f"Bearer {bearer_token}",
    "accept":"application/json"   
    }
  
    response = requests.get(api_url, headers=headers)
    data = response.json()
    return "https://image.tmdb.org/t/p/original"+data['poster_path']


def recommend(Selected_movies_name):
    movie_index = movies[movies['title'] == Selected_movies_name].index[0] 
    distance = similarity[movie_index]
    movie_list = sorted(list(enumerate(distance)),reverse=True,key=lambda x:x[1])[1:6]

    recommend_movies = []
    recommend_poster = []
    for i in movie_list:
        movie_id = movies.iloc[i[0]].movie_id
        
        recommend_movies.append(movies.iloc[i[0]].title)
        #fetch poster from API
        recommend_poster.append(fetch_poster(movie_id))
    return recommend_movies,recommend_poster    

st.title("Movie Recommender System"+':movie_camera:')

Selected_movies_name = st.selectbox('Enter you favourite Movie :clapper:',movies['title'].values)

if st.button('Recommend'):
    #st.write('<style>div.css-19y5wjw button {background-color: #BB8FCE; color: #E59866;}</style>', unsafe_allow_html=True)
    #recommendations = recommend(Selected_movies_name)
    #for i in recommendations:
    #    st.write(i)
    name,poster = recommend(Selected_movies_name)
    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        st.text(name[0])
        st.image(poster[0])
    
    with col2:
        st.text(name[1])
        st.image(poster[1])

    with col3:
        st.text(name[2])
        st.image(poster[2])

    with col4:
        st.text(name[3])
        st.image(poster[3])

    with col5:
        st.text(name[4])
        st.image(poster[4])

    
    
st.markdown(
    """
    <style>
    .stApp {
        background-color: #F9E79F ;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

custom_css = """
<style>
    /* Apply the font to the entire page */
    body {
        font-family: 'Arial', sans-serif; /* Change 'Arial' to your desired font */
    }
    /* Apply the font to specific elements, e.g., headers */
    h1, h2, h3 {
        font-family: 'Verdana', sans-serif; /* Change 'Verdana' to your desired font */
    }
     h1, h2, h3, .css-1kv3b56 {
        color: 060606; /* Change 'blue' to your desired color */
    }
    
</style>
"""

     