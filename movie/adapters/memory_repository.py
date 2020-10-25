from abc import ABC

import csv
import os
from datetime import date, datetime
from typing import List, Set

from bisect import bisect, bisect_left, insort_left

from werkzeug.security import generate_password_hash
from movie.adapters.repository import AbstractRepository, RepositoryException
from movie.domain.model import Movie, Director, Actor, Genre, Review, User


class MemoryRepository(AbstractRepository):
    # Articles ordered by date, not id. id is assumed unique.

    def __init__(self):
        self._users = list()
        self._movies = list()
        self._actors = set()
        self._genres = set()
        self._directors = set()
        self._reviews = list()


    def add_user(self, user: User):
        self._users.append(user)

    def get_user(self, username) -> User:
        return next((user for user in self._users if user.user_name == username), None)

    def add_movie(self, movie: Movie):
        # insort_left(self._movies, movie)
        self._movies.append(movie)

    def add_actor(self, actor: Actor):
        self._actors.add(actor)

    def add_genre(self, genre: Genre):
        self._genres.add(genre)

    def add_director(self, director: Director):
        self._directors.add(director)

    def add_review(self, review: Review):
        self._reviews.append(review)

    def get_genres(self) -> Set[Genre]:
        return self._genres

    def get_movies_by_genre(self, genrename: str) -> List[Movie]:
        matching_movies = list()
        for movie in self._movies:
            for genre in movie.genres:
                if genrename.lower() in genre.genre_name.lower():
                    matching_movies.append(movie)
                    break
        return matching_movies

    def get_movies_by_actor(self, actorname: str) -> List[Movie]:
        matching_movies = list()
        for movie in self._movies:
            for actor in movie.actors:
                if actorname.lower() in actor.actor_full_name.lower():
                    matching_movies.append(movie)
                    break
        return matching_movies

    def get_movies_by_director(self, directorname: str) -> List[Movie]:
        matching_movies = list()
        for movie in self._movies:
            if directorname.lower() in movie.director.director_full_name.lower():
                matching_movies.append(movie)
        return matching_movies

    def get_movie_by_name(self, name: str) -> Movie:
        for movie in self._movies:
            if movie.title == name:
                return movie
        return None

    def get_reviews_by_movie(self, moviename: str) -> List[Review]:
        matching_reviews = list()
        for review in self._reviews:
            if review.movie == moviename:
                matching_reviews.append(review)
        return matching_reviews


def read_csv_file(filename: str, repo: MemoryRepository):
    with open(filename, encoding='utf-8-sig') as infile:
        rows = csv.DictReader(infile)
        for row in rows:
            title = row['Title']
            description = row['Description']
            year = int(row['Year'])
            director = row['Director']
            D = Director(director.strip())
            genres = row['Genre'].split(',')
            movie = Movie(title, year)
            movie.director = D
            movie.description = description
            for genre in genres:
                G = Genre(genre.strip())
                repo.add_genre(G)
                movie.genres.append(G)
            repo.add_director(D)
            actors = row['Actors'].split(',')
            for actor in actors:
                A = Actor(actor.strip())
                repo.add_actor(A)
                movie.actors.append(A)
            # 
            runtime = int(row['Runtime (Minutes)'])
            movie.runtime_minutes = runtime
            repo.add_movie(movie)

def populate(data_path: str, repo: MemoryRepository):
    filename = os.path.join(data_path, "Data1000Movies.csv")
    read_csv_file(filename,repo)
