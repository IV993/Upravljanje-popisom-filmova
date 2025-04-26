# Glavna skripta

import tkinter as tk
from tkinter import messagebox
from database import Movie, MovieManager
from api import fetch_movie_details

class MovieApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Movie Manager")

        self.title_entry = tk.Entry(root)
        self.movie_id_entry = tk.Entry(root)
        self.output_text = tk.Text(root, height=30, width=60)

        self.setup_ui()

    def setup_ui(self):
        tk.Label(self.root, text="Unesite naziv filma:").grid(row=0, column=0)
        self.title_entry.grid(row=0, column=1)

        tk.Label(self.root, text="Unesite ID filma:").grid(row=1, column=0)
        self.movie_id_entry.grid(row=1, column=1)

        tk.Button(self.root, text="Dodaj film", command=self.add_movie_gui).grid(row=2, column=0)
        tk.Button(self.root, text="Označi kao pogledan", command=self.mark_as_watched_gui).grid(row=2, column=1)
        tk.Button(self.root, text="Obriši film", command=self.delete_movie_gui).grid(row=2, column=2)
        tk.Button(self.root, text="Prikaži sve filmove", command=self.show_all_movies).grid(row=3, column=0)
        tk.Button(self.root, text="Prikaži neodgledane filmove", command=self.show_unwatched_movies).grid(row=3, column=1)

        self.output_text.grid(row=4, column=0, columnspan=3)

    # Funkcija za prikaz svih filmova iz baze podataka u tekstualnom području
    def show_all_movies(self):
        """
        Dohvaća sve filmove iz baze podataka i prikazuje ih u tekstualnom području.
        Prikazuju se podaci o svakom filmu: ID, naziv, godina, žanr i status gledanosti.
        Ako baza nema filmova, korisniku se prikazuje poruka o tome.
        """
        movie_manager = MovieManager()
        movies = movie_manager.get_all_movies()
        self.output_text.delete(1.0, tk.END)
        if not movies:
            self.output_text.insert(tk.END, "Nema filmova u bazi.\n")
        else:
            for movie in movies:
                watched_status = "Pogledan" if movie.watched else "Nije pogledan"
                self.output_text.insert(tk.END, f"ID: {movie.id} | {movie.title} ({movie.year}) - {movie.genre} | {watched_status}\n")

    # Funkcija za prikazivanje samo neodgledanih filmova
    def show_unwatched_movies(self):
        """
        Dohvaća i prikazuje samo filmove koji nisu označeni kao pogledani.
        Ako nema neodgledanih filmova, korisniku se prikazuje poruka o tome.
        """
        movie_manager = MovieManager()
        movies = movie_manager.get_unwatched_movies()
        self.output_text.delete(1.0, tk.END)
        if not movies:
            self.output_text.insert(tk.END, "Nema neodgledanih filmova.\n")
        else:
            for movie in movies:
                self.output_text.insert(tk.END, f"ID: {movie.id} | {movie.title} ({movie.year}) - {movie.genre} | Nije pogledan\n")

    # Funkcija za dodavanje filma u bazu podataka putem korisničkog unosa
    def add_movie_gui(self):
        """
        Dodaje film u bazu podataka koristeći OMDb API za dohvat podataka o filmu.
        Korisnik unosi naziv filma, a aplikacija automatski dohvaća i sprema podatke.
        Ako film nije pronađen, korisniku se prikazuje odgovarajuća poruka.
        """
        title = self.title_entry.get()
        if title:
            movie_data = fetch_movie_details(title)
            if movie_data:
                movie = Movie(movie_data["title"], movie_data["year"], movie_data["genre"])
                movie_manager = MovieManager()
                movie_manager.add_movie(movie)
                messagebox.showinfo("Uspjeh", f"Film '{movie.title}' dodan u popis!")
                self.show_all_movies()
            else:
                messagebox.showerror("Greška", "Film nije pronađen!")
        else:
            messagebox.showwarning("Upit", "Molimo unesite naziv filma!")

    # Funkcija za označavanje filma kao pogledanog
    def mark_as_watched_gui(self):
        """
        Označava film kao pogledan u bazi podataka.
        Korisnik unosi ID filma koji želi označiti kao pogledan.
        Ako ID nije valjan, korisniku se prikazuje poruka o grešci.
        """
        try:
            movie_id = int(self.movie_id_entry.get())
            movie_manager = MovieManager()
            movie_manager.mark_as_watched(movie_id)
            messagebox.showinfo("Uspjeh", f"Film s ID {movie_id} označen kao pogledan!")
            self.show_all_movies()
        except ValueError:
            messagebox.showwarning("Greška", "Molimo unesite važeći ID filma!")

    # Funkcija za brisanje filma iz baze
    def delete_movie_gui(self):
        """
        Briše film iz baze podataka prema korisnički unesenom ID-u.
        Ako ID nije valjan, korisniku se prikazuje poruka o grešci.
        """
        try:
            movie_id = int(self.movie_id_entry.get())
            movie_manager = MovieManager()
            movie_manager.delete_movie(movie_id)
            messagebox.showinfo("Uspjeh", f"Film s ID {movie_id} obrisan iz baze!")
            self.show_all_movies()
        except ValueError:
            messagebox.showwarning("Greška", "Molimo unesite važeći ID filma!")

# Funkcija za inicijalizaciju GUI-a
def main():
    root = tk.Tk()
    app = MovieApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
