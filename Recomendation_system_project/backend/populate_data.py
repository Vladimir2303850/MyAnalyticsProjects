from backend.database import SessionLocal
from backend import models
import random

# Инициализация сессии
db = SessionLocal()

# Очистка старых данных (если были)
db.query(models.Rating).delete()
db.query(models.Movie).delete()
db.query(models.User).delete()
db.commit()

print("Очистка старых данных завершена")

# ---------- СОЗДАЕМ ПОЛЬЗОВАТЕЛЕЙ ----------
usernames = [f"user{i}" for i in range(1, 11)]
for username in usernames:
    user = models.User(username=username, password="1234")
    db.add(user)
db.commit()
print("Добавлены пользователи:", usernames)

# ---------- СОЗДАЕМ ФИЛЬМЫ ----------
genres = [
    "Action", "Drama", "Comedy", "Sci-Fi", "Thriller",
    "Fantasy", "Horror", "Adventure", "Mystery", "Romance"
]

# Немного базовых названий для реалистичности
base_titles = [
    "The Matrix", "Inception", "Interstellar", "Avatar", "The Dark Knight",
    "The Godfather", "Pulp Fiction", "Fight Club", "Gladiator", "Titanic",
    "Forrest Gump", "The Shawshank Redemption", "The Lord of the Rings",
    "The Avengers", "Iron Man", "Doctor Strange", "Guardians of the Galaxy",
    "The Prestige", "The Lion King", "Back to the Future"
]

# Генерация 100 фильмов
movies = []
for i in range(1, 101):
    title = random.choice(base_titles) + f" Part {random.randint(1, 5)}"
    genre = random.choice(genres)
    year = random.randint(1980, 2024)
    movies.append(models.Movie(title=title, genre=genre, year=year))
    db.add(movies[-1])

db.commit()
print(f"Добавлено {len(movies)} фильмов")

# ---------- СОЗДАЕМ ОЦЕНКИ ----------
ratings = []
users = db.query(models.User).all()
movies = db.query(models.Movie).all()

for _ in range(500):
    user = random.choice(users)
    movie = random.choice(movies)
    rating_value = random.randint(1, 5)

    # Проверяем, чтобы не было дубликатов оценок
    existing = db.query(models.Rating).filter_by(user_id=user.user_id, movie_id=movie.movie_id).first()
    if not existing:
        rating = models.Rating(user_id=user.user_id, movie_id=movie.movie_id, rating=rating_value)
        db.add(rating)
        ratings.append(rating)

db.commit()
print(f"Добавлено {len(ratings)} оценок")

db.close()
print("Данные успешно добавлены в базу!")
