from typing import List
from movie.domain.model import *
from movie.adapters.repository import AbstractRepository


def get_all_movies(repo: AbstractRepository ) -> List[Movie]:
    all_movies = repo._movies
    return all_movies

def get_alone_movie(moviename, repo: AbstractRepository) -> Movie:
    return repo.get_movie_by_name(moviename)

def get_comments(moviename,repo: AbstractRepository):
    return repo.get_reviews_by_movie(moviename)

def add_review_to_movie(moviename,text,repo:AbstractRepository):
    repo.add_review(Review(moviename,text,10))

def search_by_actor(keyword,repo:AbstractRepository):
    return repo.get_movies_by_actor(keyword)

def search_by_director(keyword,repo:AbstractRepository):
    return repo.get_movies_by_director(keyword)

def search_by_genre(keyword,repo:AbstractRepository):
    return repo.get_movies_by_genre(keyword)

## helper functions
def movie_to_dict(movie: Movie) -> dict:
    result = {}
    result["title"] = movie.title
    result["running_time"] = movie.runtime_minutes
    result["year"] = movie.year
    result["actors"] = "，".join([actor.actor_full_name for actor in movie.actors])
    result["director"] = movie.director.director_full_name
    result["genre"] = ", ".join([genre.genre_name for genre in movie.genres])
    result["description"] = movie.description
    return result
