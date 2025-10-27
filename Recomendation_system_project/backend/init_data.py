from .database import SessionLocal
from . import models

db = SessionLocal()

movies = [
    {"title": "Inception", "genre": "Sci-Fi", "year": 2010},
    {"title": "The Dark Knight", "genre": "Action", "year": 2008},
    {"title": "Interstellar", "genre": "Sci-Fi", "year": 2014},
]

for m in movies:
    db.add(models.Movie(**m))

db.commit()
db.close()
print("✅ Фильмы добавлены успешно")