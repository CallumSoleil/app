from app import app, db, models



genres_data = ['Action', 'Sci-Fi', 'Thriller', 'Comedy', 'Drama', 'Adventure', 'Fantasy', 'Horror', 'Romance', 'Animation']

genres = []
for genre_name in genres_data:
    genre = models.Genre.query.filter_by(name=genre_name).first()
    if not genre:
        genre = models.Genre(name=genre_name)
        db.session.add(genre)
    genres.append(genre)

db.session.commit()

# Step 2: Add movies and associate them with the correct genres
movies_data = [
    ('Inception', 'A mind-bending thriller about dreams within dreams.', 2010, ['Sci-Fi', 'Thriller']),
    ('The Dark Knight', 'Batman faces his greatest enemy, the Joker.', 2008, ['Action', 'Thriller']),
    ('Guardians of the Galaxy', 'A group of intergalactic criminals must pull together to stop a fanatical warrior.', 2014, ['Action', 'Sci-Fi']),
    ('The Matrix', 'A computer hacker learns from mysterious rebels about the true nature of his reality and his role in the war against its controllers.', 1999, ['Sci-Fi', 'Action']),
    ('Avengers: Endgame', 'The Avengers must reunite to defeat Thanos and undo the damage caused by the Snap.', 2019, ['Action', 'Sci-Fi']),
    ('The Shawshank Redemption', 'Two imprisoned men bond over a number of years, finding solace and eventual redemption through acts of common decency.', 1994, ['Drama']),
    ('The Godfather', 'The aging patriarch of an organized crime dynasty transfers control of his clandestine empire to his reluctant son.', 1972, ['Drama', 'Crime']),
    ('Forrest Gump', 'The presidencies of Kennedy and Johnson, the Vietnam War, the Watergate scandal and other historical events unfold from the perspective of an Alabama man with an extraordinary ability to run.', 1994, ['Drama', 'Romance']),
    ('The Lion King', 'Lion prince Simba and his father are targeted by his bitter uncle, who wants to ascend the throne himself.', 1994, ['Animation', 'Adventure']),
    ('The Dark Knight Rises', 'Eight years after the Joker’s reign of anarchy, the dark knight reappears to stop a new villain, Bane.', 2012, ['Action', 'Thriller']),
    ('Star Wars: Episode IV - A New Hope', 'Luke Skywalker joins forces with allies to rescue Princess Leia and stop the Empire from using a superweapon to destroy the galaxy.', 1977, ['Action', 'Sci-Fi']),
    ('Interstellar', 'A team of explorers travel through a wormhole in space in an attempt to ensure humanity\'s survival.', 2014, ['Sci-Fi', 'Adventure']),
    ('The Prestige', 'Two magicians engage in a bitter rivalry, with each trying to outdo the other in a series of increasingly elaborate tricks.', 2006, ['Drama', 'Mystery']),
    ('Mad Max: Fury Road', 'In a post-apocalyptic wasteland, Max teams up with a runaway named Furiosa to escape a tyrannical warlord.', 2015, ['Action', 'Adventure']),
    ('The Social Network', 'The story of how Mark Zuckerberg became the founder of Facebook.', 2010, ['Drama']),
    ('Toy Story', 'A cowboy doll is profoundly threatened and jealous when a new spaceman figure supplants him as top toy in a boy\'s room.', 1995, ['Animation', 'Adventure']),
    ('Pulp Fiction', 'The lives of two mob hitmen, a boxer, a gangster\'s wife, and a pair of diner bandits intertwine in four tales of violence and redemption.', 1994, ['Crime', 'Drama']),
    ('The Silence of the Lambs', 'A young FBI cadet must confide in an incarcerated and manipulative killer to receive his help on catching another serial killer who skins his victims.', 1991, ['Thriller', 'Crime']),
    ('The Avengers', 'Earth\'s mightiest heroes must come together to stop Loki and his alien army from enslaving humanity.', 2012, ['Action', 'Sci-Fi']),
    ('Joker', 'In Gotham City, a failed comedian with mental health issues becomes the criminal mastermind known as Joker.', 2019, ['Crime', 'Drama']),
    ('The Grand Budapest Hotel', 'The adventures of Gustave H, a concierge at a famous European hotel between the wars, and Zero Moustafa, the lobby boy who becomes his most trusted friend.', 2014, ['Comedy', 'Drama']),
    ('Blade Runner 2049', 'A young blade runner\'s discovery of a long-buried secret leads him to track down former blade runner Rick Deckard, who has been missing for thirty years.', 2017, ['Sci-Fi', 'Thriller']),
    ('Schindler\'s List', 'In German-occupied Poland during WWII, Oskar Schindler gradually becomes concerned for his Jewish workforce after witnessing their persecution by the Nazis.', 1993, ['Drama', 'History']),
    ('Catch Me If You Can', 'A seasoned FBI agent pursues Frank Abagnale, who has successfully performed cons worth millions of dollars by posing as a Pan American World Airways pilot, a Georgia parish district attorney, and a pediatrician.', 2002, ['Comedy', 'Drama']),
    ('La La Land', 'A jazz musician and an aspiring actress fall in love, but their ambitions threaten to tear them apart.', 2016, ['Romance', 'Drama']),
    ('The Wolf of Wall Street', 'Based on the true story of Jordan Belfort, from his rise to his fall as a stockbroker who engaged in corrupt practices.', 2013, ['Drama', 'Comedy']),
    ('The Revenant', 'A frontiersman on a fur trading expedition in the 1820s fights for survival after being mauled by a bear and left for dead by members of his own hunting team.', 2015, ['Drama', 'Adventure']),
]

# Step 3: Add movies and their associated genres
for title, description, release, genre_names in movies_data:
    movie = models.Movie(title=title, description=description, release=release)
    db.session.add(movie)
    db.session.commit()

    # After the movie is committed, fetch the movie object again
    movie_instance = models.Movie.query.filter_by(title=title).first()

    # Link the genres to the movie
    for genre_name in genre_names:
        genre = models.Genre.query.filter_by(name=genre_name).first()

        # Ensure the genre exists before appending
        if genre:
            movie_instance.genres.append(genre)

db.session.commit()

print("Movies and genres have been successfully added to the database!")
