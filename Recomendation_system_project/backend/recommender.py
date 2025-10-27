import pandas as pd
import numpy as np
from sqlalchemy.orm import Session
from sklearn.metrics.pairwise import cosine_similarity
from . import models


def get_user_based_recommendations(db: Session, user_id: int, top_n: int = 5):
    ratings = db.query(models.Rating).all()
    movies = db.query(models.Movie).all()
    if not ratings:
        return []

    # Преобразуем данные в DataFrame
    data = [
        {"user_id": r.user_id, "movie_id": r.movie_id, "rating": r.rating}
        for r in ratings
    ]
    df = pd.DataFrame(data)

    # Строим матрицу user-movie
    rating_matrix = df.pivot_table(index="user_id", columns="movie_id", values="rating").fillna(0)

    if user_id not in rating_matrix.index:
        return []

    # Считаем cosine similarity между пользователями
    similarity = cosine_similarity(rating_matrix)
    similarity_df = pd.DataFrame(similarity, index=rating_matrix.index, columns=rating_matrix.index)

    # Находим N самых похожих пользователей
    similar_users = similarity_df[user_id].sort_values(ascending=False).iloc[1:6].index.tolist()

    # Получаем оценки фильмов похожих пользователей
    similar_ratings = rating_matrix.loc[similar_users]

    # Средние оценки этих фильмов
    mean_ratings = similar_ratings.mean().sort_values(ascending=False)

    # Фильмы, которые пользователь ещё не оценил
    user_rated = set(df[df["user_id"] == user_id]["movie_id"])
    recommendations = [mid for mid in mean_ratings.index if mid not in user_rated]

    # Берём top_n фильмов
    top_movies = recommendations[:top_n]

    # Возвращаем информацию о фильмах
    result = []
    for movie_id in top_movies:
        movie = next((m for m in movies if m.movie_id == movie_id), None)
        if movie:
            result.append({
                "movie_id": movie.movie_id,
                "title": movie.title,
                "genre": movie.genre,
                "year": movie.year
            })

    return result
