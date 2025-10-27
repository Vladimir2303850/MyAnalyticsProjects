from sqlalchemy.orm import Session
from . import models, schemas


# --- Users ---
def create_user(db: Session, user: schemas.UserCreate):
    db_user = models.User(**user.dict())
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def get_users(db: Session):
    return db.query(models.User).all()


# --- Movies ---
def create_movie(db: Session, movie: schemas.MovieCreate):
    db_movie = models.Movie(**movie.dict())
    db.add(db_movie)
    db.commit()
    db.refresh(db_movie)
    return db_movie


def get_movies(db: Session):
    return db.query(models.Movie).all()


# --- Ratings ---
def create_rating(db: Session, rating: schemas.RatingCreate):
    db_rating = models.Rating(**rating.dict())
    db.add(db_rating)
    db.commit()
    db.refresh(db_rating)
    return db_rating


def get_ratings(db: Session):
    return db.query(models.Rating).all()


# --- Recommendations ---
def get_recommendations(db: Session, user_id: int):
    user_ratings = db.query(models.Rating).filter(models.Rating.user_id == user_id).all()

    if not user_ratings:
        return []

    favorite_genres = [r.movie.genre for r in user_ratings if r.rating >= 4]
    if not favorite_genres:
        return []

    recommended_movies = (
        db.query(models.Movie)
        .filter(models.Movie.genre.in_(favorite_genres))
        .all()
    )

    return recommended_movies
