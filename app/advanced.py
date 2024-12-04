from app import app, db, models
from flask_login import current_user

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
    list_user_genres = list(order_user_genres.items())
    list_top_movies = list(order_top_movies.items())

    user_genres_size = len(order_genre_count)

    recommended_movies = []

    # If no genres saved then show top ten movies
    if user_genres_size == 0:
        recommended_movies = list_top_movies[:10]
        message="Here are some top movies other users liked"
    elif user_genres_size == 1:
        for id, count in order_top_movies:
            movie = db.session.query(models.Movie).filter_by(id=movie_id)
            movie_genres = [genre.id for genre in movie.genres]
            if list_user_genres[0].id in movie_genres:
                recommended_movies.append(id)
    elif user_genres_size == 2:
        for id, count in order_top_movies:
            movie = db.session.query(models.Movie).filter_by(id=movie_id)
            movie_genres = [genre.id for genre in movie.genres]
            if list_user_genres[0].id in movie_genres:
                recommended_movies.append(id)
        recommended_movies = recommended_movies[:6]
        for id, count in order_top_movies:
            movie = db.session.query(models.Movie).filter_by(id=movie_id)
            movie_genres = [genre.id for genre in movie.genres]
            if list_user_genres[1].id in movie_genres:
                recommended_movies.append(id)
        recommended_movies = recommended_movies[:10]
    else:
        for id, count in order_top_movies:
            movie = db.session.query(models.Movie).filter_by(id=movie_id)
            movie_genres = [genre.id for genre in movie.genres]
            if list_user_genres[0].id in movie_genres:
                recommended_movies.append(id)
        recommended_movies = recommended_movies[:5]

        for id, count in order_top_movies:
            movie = db.session.query(models.Movie).filter_by(id=movie_id)
            movie_genres = [genre.id for genre in movie.genres]
            if list_user_genres[1].id in movie_genres:
                recommended_movies.append(id)
        recommended_movies = recommended_movies[:8]

        for id, count in order_top_movies:
            movie = db.session.query(models.Movie).filter_by(id=movie_id)
            movie_genres = [genre.id for genre in movie.genres]
            if list_user_genres[2].id in movie_genres:
                recommended_movies.append(id)
        recommended_movies = recommended_movies[:10]

    if user_genres_size != 0:
        message = "Here are some recommended movies based on you watchlist"
    return message, recommended_movies