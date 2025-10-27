from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from backend import models, schemas, crud
from backend.database import SessionLocal, engine
from backend.recommender import get_user_based_recommendations

# --- Создание таблиц ---
models.Base.metadata.create_all(bind=engine)

# --- Инициализация приложения ---
app = FastAPI(title="Movie Recommendation API")

# --- Разрешаем запросы с фронтенда ---
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- Подключение к БД ---
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# ---------- USERS ----------
@app.post("/users", response_model=schemas.UserResponse)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    existing = crud.get_user_by_username(db, user.username)
    if existing:
        return existing  # если пользователь уже есть
    return crud.create_user(db, user)


@app.get("/users", response_model=list[schemas.UserResponse])
def get_users(db: Session = Depends(get_db)):
    return crud.get_users(db)


@app.get("/users/{username}", response_model=schemas.UserResponse)
def get_user_by_name(username: str, db: Session = Depends(get_db)):
    """Эндпоинт для входа по имени"""
    user = crud.get_user_by_username(db, username)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


# ---------- MOVIES ----------
@app.post("/movies", response_model=schemas.MovieResponse)
def create_movie(movie: schemas.MovieCreate, db: Session = Depends(get_db)):
    return crud.create_movie(db, movie)


@app.get("/movies", response_model=list[schemas.MovieResponse])
def get_movies(db: Session = Depends(get_db)):
    return crud.get_movies(db)


# ---------- RATINGS ----------
@app.post("/ratings", response_model=schemas.RatingResponse)
def create_rating(rating: schemas.RatingCreate, db: Session = Depends(get_db)):
    return crud.create_rating(db, rating)


@app.get("/ratings", response_model=list[schemas.RatingResponse])
def get_ratings(db: Session = Depends(get_db)):
    return crud.get_ratings(db)


# ---------- RECOMMENDATIONS (ML) ----------
@app.get("/recommendations/{user_id}", response_model=list[schemas.MovieResponse])
def get_recommendations(user_id: int, db: Session = Depends(get_db)):
    recs = get_user_based_recommendations(db, user_id)
    if not recs:
        return []
    return recs


# ---------- Тест базы ----------
@app.get("/test-db")
def test_database(db: Session = Depends(get_db)):
    users_count = db.query(models.User).count()
    movies_count = db.query(models.Movie).count()
    ratings_count = db.query(models.Rating).count()
    return {
        "users_count": users_count,
        "movies_count": movies_count,
        "ratings_count": ratings_count
    }
