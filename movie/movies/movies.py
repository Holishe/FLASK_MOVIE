from datetime import date

from flask import Blueprint
from flask import request, render_template, redirect, url_for, session
import movie.movies.services as services

import movie.adapters.repository as repo
from better_profanity import profanity
from flask_wtf import FlaskForm
from wtforms import TextAreaField, HiddenField, SubmitField, IntegerField, SelectField, StringField
from wtforms.validators import DataRequired, Length, ValidationError, NumberRange

from movie.authentication.authentication import login_required

# Configure Blueprint.
movie_blueprint = Blueprint('movies_bp', __name__)

@movie_blueprint.route('/movies/',methods=['GET'])
def print_all_movies():
    movies_per_page = 5

    # Read query parameters.
    cursor = request.args.get('cursor')
    if cursor is None:
        # No cursor query parameter, so initialise cursor to start at the beginning.
        cursor = 0
    else:
        # Convert cursor from string to int.
        cursor = int(cursor)

    # Retrieve movies and parse them to dict
    movies = [services.movie_to_dict(i) for i in services.get_all_movies(repo.repo_instance)]

    specific_movies = movies[cursor:cursor + movies_per_page]

    first_movie_url = None
    last_movie_url = None
    next_movie_url = None
    prev_movie_url = None

    if cursor > 0:
        # There are preceding movies, so generate URLs for the 'previous' and 'first' navigation buttons.
        prev_movie_url = url_for('movies_bp.print_all_movies', cursor=cursor - movies_per_page)
        first_movie_url = url_for('movies_bp.print_all_movies')

    if cursor + movies_per_page < len(movies):
        # There are further articles, so generate URLs for the 'next' and 'last' navigation buttons.
        next_movie_url = url_for('movies_bp.print_all_movies', cursor=cursor + movies_per_page)

        last_cursor = movies_per_page * int(len(movies) / movies_per_page)
        if len(movies) % movies_per_page == 0:
            last_cursor -= movies_per_page
        last_movie_url = url_for('movies_bp.print_all_movies', cursor=last_cursor)

    # Generate the webpage to display the movies.
    return render_template(
        'movies/movielist.html',
        movies=specific_movies,
        first_movie_url=first_movie_url,
        last_movie_url=last_movie_url,
        prev_movie_url=prev_movie_url,
        next_movie_url=next_movie_url,
    )

@movie_blueprint.route('/movie/',methods=['GET','POST'])
def print_alone_movie():
    if request.method == 'POST':
        text = request.form.get('comment')
        moviename = request.form.get('moviename')
        services.add_review_to_movie(moviename,text,repo.repo_instance)
    else:
        moviename = request.args.get('moviename')
    movie = services.movie_to_dict(services.get_alone_movie(moviename,repo.repo_instance))
    comments = services.get_comments(moviename,repo.repo_instance)
    # print(comments)
    commentform = CommentForm()
    return render_template('/movies/amovie.html',amovie = movie,comments = comments, form = commentform)

@movie_blueprint.route('/search/',methods=['GET','POST'])
def print_movies_by_search():
    movies_per_page = 5

    # Read query parameters.
    cursor = request.args.get('cursor')
    if cursor is None:
        # No cursor query parameter, so initialise cursor to start at the beginning.
        cursor = 0
    else:
        # Convert cursor from string to int.
        cursor = int(cursor)
    # Read keyword and search_method
    if request.method == 'GET':
        keyword = session.get('keyword')
        option = session.get('option')
    else:
        keyword = request.form.get('keyword')
        option = request.form.get('option')
        session['keyword'] = keyword
        session['option'] = option
        cursor = 0
    # Retrieve movies and parse them to dict
    if option == 'Actor':
        movies = [services.movie_to_dict(i) for i in services.search_by_actor(keyword,repo.repo_instance)]
    elif option == 'Director':
        movies = [services.movie_to_dict(i) for i in services.search_by_director(keyword,repo.repo_instance)]
    elif option == 'Genre':
        movies = [services.movie_to_dict(i) for i in services.search_by_genre(keyword,repo.repo_instance)]
    else:
        movies = []

    specific_movies = movies[cursor:cursor + movies_per_page]

    first_movie_url = None
    last_movie_url = None
    next_movie_url = None
    prev_movie_url = None

    if cursor > 0:
        # There are preceding movies, so generate URLs for the 'previous' and 'first' navigation buttons.
        prev_movie_url = url_for('movies_bp.print_movies_by_search', cursor=cursor - movies_per_page)
        first_movie_url = url_for('movies_bp.print_movies_by_search')

    if cursor + movies_per_page < len(movies):
        # There are further articles, so generate URLs for the 'next' and 'last' navigation buttons.
        next_movie_url = url_for('movies_bp.print_movies_by_search', cursor=cursor + movies_per_page)

        last_cursor = movies_per_page * int(len(movies) / movies_per_page)
        if len(movies) % movies_per_page == 0:
            last_cursor -= movies_per_page
        last_movie_url = url_for('movies_bp.print_movies_by_search', cursor=last_cursor)

    form = SearchForm()
    # Generate the webpage to display the movies.
    return render_template(
        'movies/movielist_search.html',
        movies=specific_movies,
        first_movie_url=first_movie_url,
        last_movie_url=last_movie_url,
        prev_movie_url=prev_movie_url,
        next_movie_url=next_movie_url,
        form=form
    )

class ProfanityFree:
    def __init__(self, message=None):
        if not message:
            message = u'Field must not contain profanity'
        self.message = message

    def __call__(self, form, field):
        if profanity.contains_profanity(field.data):
            raise ValidationError(self.message)


class CommentForm(FlaskForm):
    comment = TextAreaField('Comment', [
        DataRequired(),
        Length(min=4, message='Your comment is too short'),
        ProfanityFree(message='Your comment must not contain profanity')])
    username = HiddenField('username')
    moviename = HiddenField("moviename")
    submit = SubmitField('Submit')

class SearchForm(FlaskForm):
    option = SelectField('Option: ', choices=["Actor", "Director" ,"Genre"])
    keyword = StringField('Keyword: ', [
        DataRequired()
    ])
    submit = SubmitField('Submit')
