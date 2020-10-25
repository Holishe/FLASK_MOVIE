import csv
import datetime

class Genre:
    def __init__(self, genre_name):
        if genre_name == "":
            genre_name = None
        self._genre_name = genre_name

    @property
    def genre_name(self):
        return self._genre_name

    @genre_name.setter
    def genre_name(self, value):
        self._genre_name = value

    def __repr__(self):
        return f"<Genre {self._genre_name}>"

    def __eq__(self, other):
        return self._genre_name == other.genre_name

    def __lt__(self, other):
        return self._genre_name < other.genre_name

    def __hash__(self):
        return hash(self._genre_name)


class Actor:
    def __init__(self, actor_full_name: str):
        if actor_full_name == "" or type(actor_full_name) is not str:
            self.__actor_full_name = None
        else:
            self.__actor_full_name = actor_full_name.strip()
        self._colleagues = []

    @property
    def actor_full_name(self) -> str:
        return self.__actor_full_name

    def __repr__(self):
        return f'<Actor {self.__actor_full_name}>'

    def __eq__(self, other):
        if not isinstance(other, Actor):
            return False
        else:
            return self.__actor_full_name == other.__actor_full_name

    def __lt__(self, other):
        return self.__actor_full_name < other.__actor_full_name

    def __hash__(self):
        return hash(self.__actor_full_name)

    def add_actor_colleague(self, colleague):
        self._colleagues.append(colleague)

    def check_if_this_actor_worked_with(self, colleague):
        return colleague in self._colleagues


class Director:

    def __init__(self, director_full_name: str):
        if director_full_name == "" or type(director_full_name) is not str:
            self._director_full_name = None
        else:
            self._director_full_name = director_full_name.strip()

    @property
    def director_full_name(self) -> str:
        return self._director_full_name

    def __repr__(self):
        return f"<Director {self._director_full_name}>"

    def __eq__(self, other):
        # TODO
        return self.director_full_name == other.director_full_name

    def __lt__(self, other):
        # TODO
        return self._director_full_name < other.director_full_name

    def __hash__(self):
        # TODO
        return hash(self.director_full_name)


class Movie:

    def __init__(self, title, year):

        if year < 1900:
            print("Year must not be less than 1900")
            return
        if title == "":
            print("Title is mandatory")
            return
        self.__title = title.strip()
        self.__description = None
        self.__year = year
        self.__director = None
        self.__actors = []
        self.__genres = []
        self.__runtime_minutes = 0

    @property
    def year(self):
        return self.__year

    @property
    def title(self):
        return self.__title

    @title.setter
    def title(self, title):
        self.__title = title.strip()

    @property
    def description(self):
        return self.__description

    @description.setter
    def description(self, description):
        self.__description = description.strip()

    @property
    def director(self):
        return self.__director

    @director.setter
    def director(self, value):
        self.__director = value

    @property
    def actors(self):
        return self.__actors

    @actors.setter
    def actors(self, value):
        self.__actors = value

    @property
    def genres(self):
        return self.__genres

    @genres.setter
    def genres(self, value):
        self.__genres = value

    @property
    def runtime_minutes(self):
        return self.__runtime_minutes

    @runtime_minutes.setter
    def runtime_minutes(self, runtime_minutes):
        if runtime_minutes <= 0:
            raise ValueError("Runtime must be a positive number")
        self.__runtime_minutes = runtime_minutes

    def __repr__(self):
        return f"<Movie {self.__title}, {self.__year}>"

    def __eq__(self, other):
        return isinstance(other, Movie) and self.__title == other.__title and self.__year == other.__year

    def __lt__(self, other):
        return (self.__title, self.__year) < (other.__title, other.__year)

    def __hash__(self):
        return hash(self.title + str(self.year))

    def add_actor(self, value):
        if value not in self.__actors:
            self.__actors.append(value)

    def remove_actor(self, actor):
        if actor in self.__actors:
            self.__actors.remove(actor)

    def add_genre(self, genre):
        if genre not in self.__genres:
            self.__genres.append(genre)

    def remove_genre(self, genre):
        if genre in self.__genres:
            self.__genres.remove(genre)



class MovieFileCSVReader:

    def __init__(self, file_name: str):
        self.__file_name = file_name
        self.__movies = []
        self.__actors = set()
        self.__directors = set()
        self.__genres = set()

    @property
    def dataset_of_movies(self):
        return self.__movies

    @property
    def dataset_of_actors(self):
        return self.__actors

    @property
    def dataset_of_directors(self):
        return self.__directors

    @property
    def dataset_of_genres(self):
        return self.__genres

    def read_csv_file(self):
        with open(self.__file_name, mode='r', encoding='utf-8-sig') as csvfile:
            rows = csv.DictReader(csvfile)
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
                    self.__genres.add(G)
                    movie.genres.append(G)
                self.__directors.add(D)
                actors = row['Actors'].split(',')
                for actor in actors:
                    A = Actor(actor.strip())
                    self.__actors.add(A)
                    movie.actors.append(A)

                runtime = int(row['Runtime (Minutes)'])
                movie.runtime_minutes = runtime
                self.__movies.append(movie)

class Review:
    # movie
    # review text
    # rating 1-10
    # timestamp

    def __init__(self, movie, review_text, rating):
        self.__movie = movie
        self.__review_text = review_text
        if 1 <= rating <= 10:
            self.__rating = rating
        else:
            self.__rating = None
        self.__timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%m')

    @property
    def movie(self):
        return self.__movie

    @property
    def review_text(self):
        return self.__review_text

    @property
    def rating(self):
        return self.__rating

    @property
    def timestamp(self):
        return self.__timestamp

    def __repr__(self):
        return f'Review: {self.__review_text}. Rating: {self.__rating}'

    def __eq__(self, other):
        if not isinstance(other, Review):
            return False
        else:
            return self.__movie == other.__movie and self.__rating == other.__rating and self.__timestamp == other.__timestamp and self.__review_text == other.__review_text

class User:
    def __init__(self, username, password):
        self.__user_name = username.strip().lower()
        self.__password = password
        self.__watched_movies = []
        self.__reviews = []
        self.__time_spent_watching_movies_minutes = int()

    @property
    def user_name(self):
        return self.__user_name

    @property
    def password(self):
        return self.__password

    @property
    def watched_movies(self):
        return self.__watched_movies

    @property
    def reviews(self):
        return self.__reviews

    @property
    def time_spent_watching_movies_minutes(self):
        return self.__time_spent_watching_movies_minutes

    # defines the unique string representation of the object
    def __repr__(self):
        return "<User " + self.__user_name + ">"

    # check for equality of two User object instances by comparing the user_name
    def __eq__(self, other):
        return self.__user_name == other.user_name

    # check for equality of two User object instances by comparing the names
    def __lt__(self, other):
        return self.__user_name < other.user_name

    # defines which attribute is used for computing a hash value as used in set or dictionary keys
    def __hash__(self):
        return hash(self.__user_name)

    # this method implements the action of a user watching a movie
    def watch_movie(self, movie):
        if movie not in self.__watched_movies:
            self.__watched_movies.append(movie)
            self.__time_spent_watching_movies_minutes += movie.runtime_minutes

    # this method adds a review that this user has written to the list of all reviews written by this user
    def add_review(self, review):
        if review not in self.__reviews:
            self.__reviews.append(review)