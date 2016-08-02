"""Utility file to seed ratings database from MovieLens data in seed_data/"""

from sqlalchemy import func
from model import User
from model import Rating
from model import Movie

from model import connect_to_db, db
from server import app

import datetime


def load_users():
    """Load users from u.user into database."""

    print "Users"

    # Delete all rows in table, so if we need to run this a second time,
    # we won't be trying to add duplicate users
    User.query.delete()

    # Read u.user file and insert data
    for row in open("seed_data/u.user"):
        row = row.rstrip()
        user_id, age, gender, occupation, zipcode = row.split("|")

        user = User(user_id=user_id,
                    age=age,
                    zipcode=zipcode)

        # We need to add to the session or it won't ever be stored
        db.session.add(user)

    # Once we're done, we should commit our work
    db.session.commit()


def load_movies():
    """Load movies from u.item into database."""

    print "Movies"

    # Delete all rows in table, so if we need to run this a second time,
    # we won't be trying to add duplicate users
    Movie.query.delete()
    
# movie id | movie title | release date | video release date |
# IMDb URL | unknown | Action | Adventure | Animation |
# Children's | Comedy | Crime | Documentary | Drama | Fantasy |
# Film-Noir | Horror | Musical | Mystery | Romance | Sci-Fi |
# Thriller | War | Western |

# , unknown, action, adventure, animation, children, comedy, crime, documentary, drama, fantasy, film_noir, horror, musical, mystery, romance, sci_fi, thriller, war, western 

    # Read u.user file and insert data
    for row in open("seed_data/u.item"):
        row = row.rstrip()
        row = row.split("|")
        #put in dummy thing for blank space
        movie_id, title, release_info, blank, imdb_url = row[0], row[1][:-7], row[2], row[3], row[4]
     
        if release_info:
            release_date = datetime.datetime.strptime(release_info, "%d-%b-%Y")
        else:
            release_date = None

        movie = Movie(title=title,
                    release_date=release_date,
                    imdb_url=imdb_url)

        # We need to add to the session or it won't ever be stored
        db.session.add(movie)

    # Once we're done, we should commit our work
    db.session.commit()


def load_ratings():
    """Load ratings from u.data into database."""

    print "Ratings"

    # Delete all rows in table, so if we need to run this a second time,
    # we won't be trying to add duplicate users
    Rating.query.delete()

# user_id \t movie_id \t score \t timestamp.

    # Read u.user file and insert data
    for row in open("seed_data/u.data"):
        row = row.rstrip()
        row = row.split("\t")
        user_id, movie_id, score, timestamp = row

        rating = Rating(user_id=user_id,
                    movie_id=movie_id,
                    score=score)

        # We need to add to the session or it won't ever be stored
        db.session.add(rating)

    # Once we're done, we should commit our work
    db.session.commit()


def set_val_user_id():
    """Set value for the next user_id after seeding database"""

    # Get the Max user_id in the database
    result = db.session.query(func.max(User.user_id)).one()
    max_id = int(result[0])

    # Set the value for the next user_id to be max_id + 1
    query = "SELECT setval('users_user_id_seq', :new_id)"
    db.session.execute(query, {'new_id': max_id + 1})
    db.session.commit()


if __name__ == "__main__":
    connect_to_db(app)

    # In case tables haven't been created, create them
    db.create_all()

    # Import different types of data
    load_users()
    load_movies()
    load_ratings()
    set_val_user_id()