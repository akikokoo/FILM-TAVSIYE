import requests
from bs4 import BeautifulSoup
from openpyxl import Workbook


categoryList = ["action","adventure","animation","biography","comedy","crime","drama","family","fantasy","film_noir","history","horror","musical","music","mystery","romance","sci_fi","sport","thriller","war","western"]
gnrList = ["1","2","3","4","5","6","7","8","9","10","11","12","13","14","15","16","17","18","19","20","21"]


def save_IMDB_xl():

    # Create a new workbook and select the active sheet
    wb = Workbook()
    ws = wb.active

    # Write headers to the worksheet
    ws.append(["Rank", "Name", "Year", "Rating", "Category", "Description", "ID"])

    for category, gnr in zip(categoryList,gnrList):
        url = f"https://www.imdb.com/search/title/?genres={category}&sort=user_rating,desc&title_type=feature&num_votes=25000,&pf_rd_m=A2FGELUUNOQJNL&pf_rd_p=94365f40-17a1-4450-9ea8-01159990ef7f&pf_rd_r=7ZHT2F4Q0BQ2W9670M7G&pf_rd_s=right-6&pf_rd_t=15506&pf_rd_i=top&ref_=chttp_gnr_{gnr}"

        # Send a GET request to the URL
        response = requests.get(url)

        # Parse the HTML content using BeautifulSoup
        soup = BeautifulSoup(response.content, "html.parser")

        # Find all the movie items on the page
        movie_items = soup.find_all("div", class_="lister-item mode-advanced")

        # Iterate over each movie item and extract the required information
        for movie in movie_items:
            # Extract rank
            rank = movie.find("span", class_="lister-item-index").text.strip(".")
            
            # Extract movie name
            name = movie.find("h3", class_="lister-item-header").a.text
            
            # Extract year
            year = movie.find("span", class_="lister-item-year").text.strip("()").replace("I) (","").replace("I","")
            
            # Extract IMDB rating
            rating = movie.find("div", class_="ratings-bar").strong.text

            # Extract description
            desc = movie.find_all("p", class_="text-muted")[1].text
            
            id = movie.find("h3",class_="lister-item-header").a["href"].replace("/title/tt","").replace("/","")

            # Write the data to the worksheet
            ws.append([rank, name, year, rating, category, desc, id])

    # Save the workbook
    wb.save("C:\\Users\\Akif\\Desktop\\film\\film_list\\butun_liste.xlsx")
save_IMDB_xl()
