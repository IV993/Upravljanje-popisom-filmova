# Modul za dohvaćanje filmova s OMDb API-ja

import requests
import os
from dotenv import load_dotenv

# Učitavanje API ključa iz .env datoteke
load_dotenv()
OMDB_API_KEY = os.getenv("OMDB_API_KEY")

if not OMDB_API_KEY:
    OMDB_API_KEY = input("Unesite svoj OMDB API ključ: ")
    with open(".env", "w") as env_file:
        env_file.write(f"OMDB_API_KEY={OMDB_API_KEY}\n")

def fetch_movie_details(title):
    """
    Dohvaća detalje o filmu s OMDb API-ja prema nazivu filma.
    :param title: Naziv filma za koji želimo dohvatiti podatke
    :return: Objekt s podacima filma ili None ako film nije pronađen
    """
    url = f"http://www.omdbapi.com/?t={title}&apikey={OMDB_API_KEY}"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        if data["Response"] == "True":
            return {
                "title": data["Title"],
                "year": data["Year"],
                "genre": data["Genre"]
            }
    return None