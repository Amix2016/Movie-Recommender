from email import header
import streamlit as st
import pickle
import pandas as pd
import numpy as np
import requests

def add_bg_from_url():
    st.markdown(
         f"""
         <style>
         .stApp {{
             background-image: url("http://www.clitravi.com/wp-content/uploads/2017/07/photo-placeholder-5.jpg");
             background-attachment: fixed;
             background-size: cover
         }}
         </style>
         """,
         unsafe_allow_html=True
     )

add_bg_from_url() 

movies_dict = pickle.load(open('movie_dict.pkl','rb'))
movies = pd.DataFrame(movies_dict)

similarity1 = pickle.load(open('similarity1.pkl','rb'))
similarity2 = pickle.load(open('similarity2.pkl','rb'))
similarity = np.concatenate((similarity1, similarity2), axis=0)

st.title('Movie Recommender System')

selected_movie_name = st.selectbox(
'Select a Movie Name',
movies['title'].values)


def fetch_poster(movie_id):
  response = requests.get('https://api.themoviedb.org/3/movie/{}?api_key=e902e280d84207fab1830c37e34a9ca2&language=en-US'.format(movie_id))
  data = response.json()
  return 'https://image.tmdb.org/t/p/w500/' + data['poster_path']


def recommend(movie):
  movie_index = movies[movies['title']==movie].index[0]
  distances = similarity[movie_index]
  movie_list = sorted(list(enumerate(distances)),reverse=True,key=lambda x:x[1])[1:6]


  recommended_movies = []
  recommended_movies_poster = []

  for i in movie_list:
    movie_id = movies.iloc[i[0]].movie_id
    recommended_movies.append(movies.iloc[i[0]].title)
    # fetch poster from API
    recommended_movies_poster.append(fetch_poster(movie_id))
  
  return recommended_movies,recommended_movies_poster

if st.button('Recommend'):
    names,posters = recommend(selected_movie_name)
    
    col1, col2, col3, col4, col5 = st.columns(5)

    with col1:
      st.text(names[0])
      st.image(posters[0])

    with col2:
      st.text(names[1])
      st.image(posters[1])

    with col3:
      st.text(names[2])
      st.image(posters[2])

    with col4:
      st.text(names[3])
      st.image(posters[3])

    with col5:
      st.text(names[4])
      st.image(posters[4])
