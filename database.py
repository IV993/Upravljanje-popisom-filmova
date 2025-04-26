# Modul za rad s bazom podataka

import sqlite3

# Klasa Movie predstavlja film sa svim potrebnim atributima
class Movie:
    def __init__(self, title, year, genre, watched=False, movie_id=None):
        """
        Konstruktor za klasu Movie
        :param title: Naziv filma
        :param year: Godina izlaska filma
        :param genre: Žanr filma
        :param watched: Status gledanosti (default: False)
        :param movie_id: Id filma
        """
        self.id = movie_id
        self.title = title
        self.year = year
        self.genre = genre
        self.watched = watched

    def __repr__(self):
        return f"Movie(title={self.title}, year={self.year}, genre={self.genre}, watched={self.watched}, movie_id={self.id})"

# Klasa MovieManager omogućuje rad s filmovima u bazi podataka
class MovieManager:
    def __init__(self, db_name="movies.db"):
        """
        Konstruktor za klasu MovieManager
        :param db_name: Naziv SQLite baze podataka
        """
        self.db_name = db_name

    def create_table(self):
        """
        Kreira tablicu za pohranu filmova ako ne postoji.
        """
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            cursor.execute('''CREATE TABLE IF NOT EXISTS movies (
                              id INTEGER PRIMARY KEY AUTOINCREMENT,
                              title TEXT,
                              year TEXT,
                              genre TEXT,
                              watched INTEGER DEFAULT 0)''')
            conn.commit()
            conn.close()

    def add_movie(self, movie: Movie):
        """
        Dodaje film u bazu podataka.
        :param movie: Objekt klase Movie
        """
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        cursor.execute("INSERT INTO movies (title, year, genre) VALUES (?, ?, ?)",
                       (movie.title, movie.year, movie.genre))
        conn.commit()
        conn.close()

    def mark_as_watched(self, movie_id: int):
        """
        Označava film kao pogledan.
        :param movie_id: ID filma koji treba označiti kao pogledan
        """
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        cursor.execute("UPDATE movies SET watched = 1 WHERE id = ?", (movie_id,))
        conn.commit()
        conn.close()

    def delete_movie(self, movie_id: int):
        """
        Briše film iz baze podataka.
        :param movie_id: ID filma koji treba obrisati
        """
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        cursor.execute("DELETE FROM movies WHERE id = ?", (movie_id,))
        conn.commit()
        conn.close()

    def get_all_movies(self):
        """
        Dohvaća sve filmove iz baze podataka.
        :return: Lista filmova
        """
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM movies")
        movies = cursor.fetchall()
        conn.close()
        return [Movie(title=movie[1], year=movie[2], genre=movie[3], watched=bool(movie[4]), movie_id=movie[0]) for movie in movies]

    def get_unwatched_movies(self):
        """
        Dohvaća samo neodgledane filmove iz baze podataka.
        :return: Lista neodgledanih filmova
        """
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM movies WHERE watched = 0")
        movies = cursor.fetchall()
        conn.close()
        return [Movie(title=movie[1], year=movie[2], genre=movie[3], watched=bool(movie[4]), movie_id=movie[0]) for movie in movies]
