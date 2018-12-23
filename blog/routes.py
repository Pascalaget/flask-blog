from flask import render_template, request
import pickle
from blog import app
from flask_msearch import Search
from  sqlalchemy.sql.expression import func
from blog.models import Movies,Movie_cast,Movie_genre,Actors,Genre

MSEARCH_INDEX_NAME = 'msearch'
MSEARCH_BACKEND = 'whoosh'
MSEARCH_ENABLE = True

search = Search()
search.init_app(app)

#index page
@app.route('/')
@app.route('/index', methods=['GET'])
def index():

    page = request.args.get('page', 1, type=int)
	#number of pages show case for pagination, 6 per page 
    per_page = 6

    posts = Movies.query.order_by(Movies.year.desc()).paginate(page=page, per_page=per_page, error_out=False)
    return render_template('index.html', posts=posts)

#sort movies a-z
@app.route('/az', methods=['POST', 'GET'])
def az():

    page = request.args.get('page', 1, type=int)
    per_page = 18

    posts = Movies.query.order_by(Movies.title.asc()).paginate(page=page, per_page=per_page, error_out=False)

    return render_template('az.html', posts=posts)

#random movies
@app.route('/rand', methods=['POST', 'GET'])
def rand():

    page = request.args.get('page', 1, type=int)
    per_page = 18

    posts = Movies.query.order_by(func.random()).paginate(page=page, per_page=per_page, error_out=False)
    return render_template('rand.html', posts=posts, rand=rand)

#movie page
@app.route('/post/<int:post_id>', methods=['GET', 'POST'])
def post(post_id):

    post = Movies.query.filter_by(movie_id=post_id).one()
    # for actors similar all posts
    posts = Movies.query.order_by(func.random()).all()
    # for similar genre remove genreless movies
    postwg = Movies.query.filter(Movies.genres is not None).order_by(func.random())

    return render_template('post.html', post=post, posts=posts, postwg=postwg)

#actor selected, show all with that actor
@app.route('/actor/<actor_id>')
def actor(actor_id):

    page = request.args.get('page', 1, type=int)
    per_page = 18

    total = Movies.query.join(Movie_cast, Movie_cast.movie_id == Movies.movie_id) \
        .join(Actors, Actors.actor_id == Movie_cast.actor_id) \
        .filter(Actors.actor_id == actor_id).order_by(Movies.movie_id.asc()).count()

    posts = Movies.query.join(Movie_cast, Movie_cast.movie_id == Movies.movie_id) \
        .join(Actors, Actors.actor_id == Movie_cast.actor_id) \
        .filter(Actors.actor_id == actor_id).order_by(Movies.movie_id.asc()).paginate(page=page, per_page=per_page,
                                                                                      error_out=False)

    clicked = Actors.query.filter(Actors.actor_id == actor_id).one()

    return render_template('actor.html', posts=posts, actor_id=actor_id, clicked=clicked, total=total)

#genre, show movies with same genre
@app.route('/genre/<genre_id>')
def genre(genre_id):

    page = request.args.get('page', 1, type=int)
    per_page = 18

    posts = Movies.query.join(Movie_genre, Movie_genre.movie_id == Movies.movie_id) \
        .join(Genre, Genre.genre_id == Movie_genre.genre_id) \
        .filter(Genre.genre_id == genre_id).order_by(Movies.movie_id.asc()).paginate(page=page, per_page=per_page,
                                                                                     error_out=False)

    total = Movies.query.join(Movie_genre, Movie_genre.movie_id == Movies.movie_id) \
        .join(Genre, Genre.genre_id == Movie_genre.genre_id) \
        .filter(Genre.genre_id == genre_id).order_by(Movies.movie_id.asc()).count()

    clicked = Genre.query.filter(Genre.genre_id == genre_id).one()

    return render_template('genre.html', posts=posts, genre_id=genre_id, clicked=clicked, total=total)

#search, search for title,content,studio
@app.route('/searchblog', methods=['POST', 'GET'])
def searchblog():
    page = request.args.get('page', 1, type=int)
    per_page = 18

    if request.method == 'POST':

        searchedword = request.form['searchitem']
        with open('searchedword.pickle', 'wb') as handle:
            pickle.dump(searchedword, handle, protocol=pickle.HIGHEST_PROTOCOL)
        posts = Movies.query.msearch(searchedword, fields=['title', 'plot', 'studio'])
        total = posts.count()
        posts = posts.paginate(page=page, per_page=per_page, error_out=False)
        return render_template('search.html', posts=posts, searchedword=searchedword, total=total)
    else:
        with open('searchedword.pickle', 'rb') as handle:
            searchedword = pickle.load(handle)
        posts = Movies.query.msearch(searchedword, fields=['title', 'plot', 'studio'])
        total = posts.count()
        posts = posts.paginate(page=page, per_page=per_page, error_out=False)
        return render_template('search.html', posts=posts, searchedword=searchedword, total=total)
