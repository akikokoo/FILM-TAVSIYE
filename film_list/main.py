import streamlit as st
import pandas as pd
import random
import os
from imdb import Cinemagoer
import random


st.set_page_config(
        page_title="Film Öneri Uygulaması",
        page_icon="🎥",
        layout="wide",
        initial_sidebar_state="expanded",
        menu_items={
            "Get Help": "https://github.com/TOBB-ETU-CS-Community",
            "Report a bug": "https://tobbetu-bilgisayar-toplulugu.streamlit.app/Geri_Bildirim_Formu",
            "About": "En İyi Film Önerileri İçin Doğru Adres!"
        },
    )


categoryList = ["action","adventure","animation","biography","comedy","crime","drama","family","fantasy","film_noir","history","horror","musical","music","mystery","romance","sci_fi","sport","thriller","war","western"]


def set_random_film_data_list(excel_file,selected_category):
    global data_list
    data_list = []

    df = pd.read_excel(excel_file)
    film_rows = df[df['Category'] == selected_category]

    names = film_rows['Name'].values
    years = film_rows['Year'].values
    ratings = film_rows['Rating'].values
    descs = film_rows["Description"].values
    id = film_rows["ID"].values
    
    if selected_category == "film_noir":
        film_number = random.randint(0,29)
    else:
        film_number = random.randint(0,49)
    
    data_list.extend([names[film_number],years[film_number],ratings[film_number],id[film_number],descs[film_number]])
    
def get_image_url(film_ID):
    ia = Cinemagoer()
    movie = ia.get_movie(film_ID)

    url = movie['cover url']
    if ('@' in url) and ('.' in url):
        url = url[:url.rindex('@') + 1] + url[url.rindex('.'):]

    base, ext = os.path.splitext(url)
    i = url.count('@')
    s2 = url.split('@')[0]
    url = s2 + '@' * i + ext
    return url

def main():

    with st.sidebar:
        st.header("Film Öneri Uygulaması")
        selected_category = st.selectbox("Kategori Seçiniz:", [category for category in categoryList],index=0)

        a = st.button("Film öner")
    if a:
        set_random_film_data_list("./butun_liste.xlsx",selected_category)
        st.image(get_image_url(data_list[3]), width=400)
        st.markdown(f'''
                <p><strong>Name:</strong>{data_list[0]}</p>
                <br />
                <p><strong>Rating:</strong>{data_list[2]}</p>
                <br />
                <p><strong>Year:</strong>{data_list[1]}</p>
                <br />
                <p><strong>Description:</strong>{data_list[4]}</p>
                <br />    
        ''',unsafe_allow_html=True)      
        

    



if __name__ == "__main__":
    main()
