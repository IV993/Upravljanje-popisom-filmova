# Glavna skripta

import tkinter as tk
from tkinter import messagebox
from database import Movie, MovieManager
from api import fetch_movie_details

# Funkcija za prikaz svih filmova iz baze podataka u tekstualnom području
def show_all_movies():
    """
    Dohvaća sve filmove iz baze podataka i prikazuje ih u tekstualnom području.
    Prikazuju se podaci o svakom filmu: ID, naziv, godina, žanr i status gledanosti.
    Ako baza nema filmova, korisniku se prikazuje poruka o tome.
    """
    movie_manager = MovieManager()
    movies = movie_manager.get_all_movies()
    output_text.delete(1.0, tk.END)  # Očistimo tekstualno područje
    if not movies:
        output_text.insert(tk.END, "Nema filmova u bazi.\n")
    else:
        for movie in movies:
            watched_status = "Pogledan" if movie.watched else "Nije pogledan"
            output_text.insert(tk.END, f"ID: {movie.id} | {movie.title} ({movie.year}) - {movie.genre} | {watched_status}\n")

# Funkcija za prikazivanje samo neodgledanih filmova
def show_unwatched_movies():
    """
    Dohvaća i prikazuje samo filmove koji nisu označeni kao pogledani.
    Ako nema neodgledanih filmova, korisniku se prikazuje poruka o tome.
    """
    movie_manager = MovieManager()
    movies = movie_manager.get_unwatched_movies()
    output_text.delete(1.0, tk.END)
    if not movies:
        output_text.insert(tk.END, "Nema neodgledanih filmova.\n")
    else:
        for movie in movies:
            output_text.insert(tk.END, f"ID: {movie.id} | {movie.title} ({movie.year}) - {movie.genre} | Nije pogledan\n")

# Funkcija za dodavanje filma u bazu podataka putem korisničkog unosa
def add_movie_gui():
    """
    Dodaje film u bazu podataka koristeći OMDb API za dohvat podataka o filmu.
    Korisnik unosi naziv filma, a aplikacija automatski dohvaća i sprema podatke.
    Ako film nije pronađen, korisniku se prikazuje odgovarajuća poruka.
    """
    title = title_entry.get()  # Dohvaćanje naziva filma iz korisničkog unosa
    if title:
        movie_data = fetch_movie_details(title)  # Dohvaćanje podataka o filmu s OMDb API-ja
        if movie_data:
            movie = Movie(movie_data["title"], movie_data["year"], movie_data["genre"])
            movie_manager = MovieManager()
            movie_manager.add_movie(movie)  # Dodavanje filma u bazu
            messagebox.showinfo("Uspjeh", f"Film '{movie.title}' dodan u popis!")
            show_all_movies()  # Ažuriranje popisa filmova
        else:
            messagebox.showerror("Greška", "Film nije pronađen!")  # Ako film nije pronađen u OMDb API-u
    else:
        messagebox.showwarning("Upit", "Molimo unesite naziv filma!")  # Ako naziv filma nije unesen

# Funkcija za označavanje filma kao pogledanog
def mark_as_watched_gui():
    """
    Označava film kao pogledan u bazi podataka.
    Korisnik unosi ID filma koji želi označiti kao pogledan.
    Ako ID nije valjan, korisniku se prikazuje poruka o grešci.
    """
    try:
        movie_id = int(movie_id_entry.get())  # Dohvaćanje ID-a filma
        movie_manager = MovieManager()
        movie_manager.mark_as_watched(movie_id)  # Označavanje filma kao pogledanog
        messagebox.showinfo("Uspjeh", f"Film s ID {movie_id} označen kao pogledan!")
        show_all_movies()  # Ažuriranje popisa filmova
    except ValueError:
        messagebox.showwarning("Greška", "Molimo unesite važeći ID filma!")  # Ako uneseni ID nije broj

# Funkcija za brisanje filma iz baze
def delete_movie_gui():
    """
    Briše film iz baze podataka prema korisnički unesenom ID-u.
    Ako ID nije valjan, korisniku se prikazuje poruka o grešci.
    """
    try:
        movie_id = int(movie_id_entry.get())  # Dohvaćanje ID-a filma
        movie_manager = MovieManager()
        movie_manager.delete_movie(movie_id)  # Brisanje filma iz baze
        messagebox.showinfo("Uspjeh", f"Film s ID {movie_id} obrisan iz baze!")
        show_all_movies()  # Ažuriranje popisa filmova
    except ValueError:
        messagebox.showwarning("Greška", "Molimo unesite važeći ID filma!")  # Ako uneseni ID nije broj

# Funkcija za inicijalizaciju GUI-a
def main():
    """
    Glavna funkcija za inicijalizaciju GUI-a aplikacije.
    Postavlja sve potrebne komponente za korisničko sučelje i povezuje ih s funkcijama.
    """
    global title_entry, movie_id_entry, output_text  # Globalno za pristup unutar funkcija

    # Kreiranje glavnog prozora
    root = tk.Tk()
    root.title("Movie Manager")

    # Kreiranje okvira za unos naziva filma
    title_label = tk.Label(root, text="Unesite naziv filma:")
    title_label.grid(row=0, column=0)
    title_entry = tk.Entry(root)
    title_entry.grid(row=0, column=1)

    # Kreiranje okvira za unos ID-a filma
    movie_id_label = tk.Label(root, text="Unesite ID filma:")
    movie_id_label.grid(row=1, column=0)
    movie_id_entry = tk.Entry(root)
    movie_id_entry.grid(row=1, column=1)

    # Kreiranje gumba za dodavanje filma
    add_movie_button = tk.Button(root, text="Dodaj film", command=add_movie_gui)
    add_movie_button.grid(row=2, column=0)

    # Kreiranje gumba za označavanje filma kao pogledanog
    mark_watched_button = tk.Button(root, text="Označi kao pogledan", command=mark_as_watched_gui)
    mark_watched_button.grid(row=2, column=1)

    # Kreiranje gumba za brisanje filma
    delete_movie_button = tk.Button(root, text="Obriši film", command=delete_movie_gui)
    delete_movie_button.grid(row=2, column=2)

    # Kreiranje gumba za prikaz svih filmova
    show_all_button = tk.Button(root, text="Prikaži sve filmove", command=show_all_movies)
    show_all_button.grid(row=3, column=0)

    # Kreiranje gumba za prikaz neodgledanih filmova
    show_unwatched_button = tk.Button(root, text="Prikaži neodgledane filmove", command=show_unwatched_movies)
    show_unwatched_button.grid(row=3, column=1)

    # Kreiranje tekstualnog područja za prikaz rezultata
    output_text = tk.Text(root, height=30, width=60)
    output_text.grid(row=4, column=0, columnspan=3)

    # Pokretanje glavne petlje aplikacije
    root.mainloop()

# Pokretanje aplikacije
if __name__ == "__main__":
    main()