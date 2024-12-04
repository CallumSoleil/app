from flask import render_template, redirect, request, flash
from app import app, db, models, login_manager
from flask_login import login_required, login_user, logout_user, current_user

app.app_context().push()

@app.route('/', methods=['GET', 'POST'])
@login_required
def movies():
    search_query = request.args.get('search', '')
    genre_ids = request.args.getlist('genres')
    query = db.session.query(models.Movie)

    # Title search
    if search_query:
        query = query.filter(models.Movie.title.ilike(f'%{search_query}%'))

    # Genre Search
    # Movies selected if at least one genre matches
    if genre_ids:
        query = query.join(models.Movie.genres).filter(models.Genre.id.in_(genre_ids))

    movies = query.distinct().all()  # Ensure distinct results
    genres = db.session.query(models.Genre).all()

    watchlist_movies = current_user.watchlist

    return render_template('all.html', title="Movies", movies=movies, genres=genres, search_query=search_query, selected_genres=genre_ids, watchlist_movies=watchlist_movies)

@app.route('/add/<int:movie_id>')
@login_required
def add(movie_id):
    movie = models.Movie.query.get(movie_id)
    add_watchlist = models.Watchlist(movie_id=movie.id, user_id=current_user.id)
    db.session.add(add_watchlist)
    db.session.commit()
    return redirect('/')

@app.route('/unadd/<int:movie_id>')
@login_required
def unadd(movie_id):
    entry = models.Watchlist.query.filter_by(user_id=current_user.id, movie_id=movie_id).first()
    if entry:
        db.session.delete(entry)
        db.session.commit()
    return redirect('/')

@app.route('/watchlist')
@login_required
def watchlist():
    return render_template('watchlist.html', title="Watchlist", movies=current_user.watchlist)


# Advanced feature page
@app.route('/recommended')
@login_required
def recommended():
    watchlist_movies = current_user.watchlist
    message, recommended_movies = user_recommendations()

    movies = db.session.query(models.Movie).filter(models.Movie.id.in_(recommended_movies)).all()
    # Reorder again
    ordered_movies = sorted(movies, key=lambda movie: recommended_movies.index(movie.id))
    return render_template('recommended.html', title="Recommended", message=message, movies=ordered_movies, watchlist=watchlist_movies)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        user = models.User.query.filter_by(username=username).first()  # Find user by username
        if user and user.password == password:
            login_user(user)
            return redirect('/')
        else:
            flash('Login failed. Try Again', 'danger')
    
    return render_template('login.html', title="Login")

@app.route('/logout')
def logout():
    logout_user()
    flash('Logged out', 'info')
    return redirect('/login')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        
        new_user = models.User(username=username, email=email, password=password)
        db.session.add(new_user)
        db.session.commit()

        return redirect('/login')
    
    return render_template('register.html', title="Register")






    #ADVANCED

def get_user_top_genres():
    # List of all genres in user watchlist with all repeats
    genres_in_watchlist = db.session.query(models.Genre).join(models.MovieGenre).join(models.Movie).join(models.Watchlist).filter(models.Watchlist.user_id==current_user.id).all()

    # Count instances of each genre
    # Dictionary made of genre.id and count
    genre_count = {}
    for genre in genres_in_watchlist:
        if genre.id in genre_count:
            genre_count[genre.id] += 1
        else:
            genre_count[genre.id] = 1

    # Order from high to low
    order_genre_count = sorted(genre_count.items(), key=lambda x:x[1], reverse=True)
    return genre_count

def get_top_new_movies():
    #List all movies that arent in the users watchlist
    movies = db.session.query(models.Movie).join(models.Watchlist).filter(models.Watchlist.user_id != current_user.id).all()
    
    # Count instances of each movie
    movie_count = {}
    for movie in movies:
        if movie.id in movie_count:
            movie_count[movie.id] += 1
        else:
            movie_count[movie.id] = 1

    # Order from high to low
    order_movie_count = sorted(movie_count.items(), key=lambda x:x[1], reverse=True)

    return order_movie_count

def user_recommendations():
    order_user_genres = get_user_top_genres()
    order_top_movies = get_top_new_movies()
    list_user_genres = list(order_user_genres)
    list_top_movies = list(order_top_movies)

    user_genres_size = len(order_user_genres)

    recommended_movies = []

    # If no genres saved then show top ten movies
    if user_genres_size == 0:
        for m_id, count in order_top_movies:
            recommended_movies.append(m_id)
        recommended_movies = recommended_movies[:10]
        message="Here are some top movies other users liked"
    elif user_genres_size == 1:
        for m_id, count in order_top_movies:
            movie = db.session.query(models.Movie).filter_by(id=m_id).first()
            movie_genres = [genre.id for genre in movie.genres]
            if list_user_genres[0] in movie_genres:
                recommended_movies.append(m_id)
    elif user_genres_size == 2:
        for m_id, count in order_top_movies:
            movie = db.session.query(models.Movie).filter_by(id=m_id).first()
            movie_genres = [genre.id for genre in movie.genres]
            if list_user_genres[0] in movie_genres:
                recommended_movies.append(m_id)
        recommended_movies = recommended_movies[:6]
        for m_id, count in order_top_movies:
            movie = db.session.query(models.Movie).filter_by(id=m_id).first()
            movie_genres = [genre.id for genre in movie.genres]
            if list_user_genres[1] in movie_genres:
                recommended_movies.append(m_id)
        recommended_movies = recommended_movies[:10]
    else:
        for m_id, count in order_top_movies:
            movie = db.session.query(models.Movie).filter_by(id=m_id).first()
            movie_genres = [genre.id for genre in movie.genres]
            if list_user_genres[0] in movie_genres:
                recommended_movies.append(m_id)
        recommended_movies = recommended_movies[:5]

        for m_id, count in order_top_movies:
            movie = db.session.query(models.Movie).filter_by(id=m_id).first()
            movie_genres = [genre.id for genre in movie.genres]
            if list_user_genres[1] in movie_genres:
                recommended_movies.append(m_id)
        recommended_movies = recommended_movies[:8]

        for m_id, count in order_top_movies:
            movie = db.session.query(models.Movie).filter_by(id=m_id).first()
            movie_genres = [genre.id for genre in movie.genres]
            if list_user_genres[2] in movie_genres:
                recommended_movies.append(m_id)
        recommended_movies = recommended_movies[:10]

    if user_genres_size != 0:
        message = "Here are some recommended movies based on you watchlist"
    return message, recommended_movies