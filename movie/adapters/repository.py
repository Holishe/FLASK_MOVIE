import abc
from typing import List, Set
from datetime import date

from movie.domain.model import Movie, Director, Actor, Genre, Review, User


repo_instance = None


class RepositoryException(Exception):

    def __init__(self, message=None):
        pass


class AbstractRepository(abc.ABC):

    @abc.abstractmethod
    def add_user(self, user: User):
        """" Adds a User to the repository. """
        raise NotImplementedError

    @abc.abstractmethod
    def get_user(self, username) -> User:
        """
        Returns the User named username from the repository.
        If there is no User with the given username, this method returns None.
        """
        raise NotImplementedError

    @abc.abstractmethod
    def add_movie(self, movie: Movie):
        """
        Adds a Movie to the repository.
        """
        raise NotImplementedError

    @abc.abstractmethod
    def add_actor(self, actor: Actor):
        """
        Adds a actor to the repository.
        """
        raise NotImplementedError

    @abc.abstractmethod
    def add_genre(self, genre: Genre):
        """
        Adds a genre to the repository.
        """
        raise NotImplementedError

    @abc.abstractmethod
    def add_director(self, director: Director):
        """
        Adds a director to the repository.
        """
        raise NotImplementedError

    @abc.abstractmethod
    def add_review(self, review: Review):
        """
        Add review
        """
        raise NotImplementedError

    @abc.abstractmethod
    def get_genres(self) -> Set[Genre]:
        """ 
        Returns all genres.
        """
        raise NotImplementedError

    @abc.abstractmethod
    def get_movies_by_genre(self, genre) -> List[Movie]:
        """
        Returns all matching movies using a genre
        """
        raise NotImplementedError

    @abc.abstractmethod
    def get_movies_by_actor(self, actor_str: str) -> List[Movie]:
        """
        Returns all matching movies using a actor
        """
        raise NotImplementedError

    @abc.abstractmethod
    def get_movies_by_director(self, director_str: str) -> List[Movie]:
        """
        Returns all matching movies using a director
        """
        raise NotImplementedError

    @abc.abstractmethod
    def get_movie_by_name(self, name: str) -> Movie:
        """
        return a movie using a id"""
        raise NotImplementedError

    @abc.abstractmethod
    def get_reviews_by_movie(self, moviename: str) -> List[Review]:
        """ 
        Returns all review using a movie
        """
        raise NotImplementedError






