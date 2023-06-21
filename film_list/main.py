import streamlit as st
import pandas as pd
import random
from butun_liste import save_IMDB_xl
import os
from imdb import Cinemagoer
import random

categoryList = ["action","adventure","animation","biography","comedy","crime","drama","family","fantasy","film_noir","history","horror","musical","music","mystery","romance","sci_fi","sport","thriller","war","western"]
global data_list

@st.cache_data
def call_save_IMDB_xl():
    return save_IMDB_xl()

@st.cache_data
def set_random_film_data_list(excel_file,selected_category):
    data_list = []

    df = pd.read_excel(excel_file)
    film_rows = df[df['Category'] == selected_category]

    names = film_rows['Name'].tolist()
    years = film_rows['Year'].tolist()
    ratings = film_rows['Rating'].tolist()
    descs = film_rows["Description"].toList()
    id = film_rows["ID"].toList()
    
    if selected_category == "film_noir":
        film_number = random.randint(0,30)
    else:
        film_number = random.randint(0,50)
    
    data_list.append(names[film_number],years[film_number],ratings[film_number],id[film_number],descs[film_number])
    
def get_image_url(film_ID):
    ia = Cinemagoer()
    movie = ia.get_movie(film_ID)

    url = movie['cover url']
    url = url[:url.rindex('@') + 1] + url[url.rindex('.'):]

    base, ext = os.path.splitext(url)
    i = url.count('@')
    s2 = url.split('@')[0]
    url = s2 + '@' * i + ext
    return url

def main():
    #retrieving
    call_save_IMDB_xl()

    with st.sidebar:
        st.header("Film Öneri Uygulaması")
        selected_category = st.selectbox("Kategori Seçiniz:", [category for category in categoryList])
        set_random_film_data_list(r"film_list\butun_liste.xlsx",selected_category)
        st.markdown('''
            <br />
            <button target="suggest">Film Öner</button>
        ''')
    st.markdown(f'''
        <img src=[{get_image_url(data_list[3])} />          
    ''')
    



if __name__ == "__main__":
    main()