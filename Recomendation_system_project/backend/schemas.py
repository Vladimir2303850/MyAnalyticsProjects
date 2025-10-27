from pydantic import BaseModel

# ---------- USERS ----------
class UserBase(BaseModel):
    username: str


class UserCreate(UserBase):
    password: str


class UserResponse(UserBase):
    user_id: int

    class Config:
        orm_mode = True


# ---------- MOVIES ----------
class MovieBase(BaseModel):
    title: str
    genre: str
    year: int


class MovieCreate(MovieBase):
    pass


class MovieResponse(MovieBase):
    movie_id: int

    class Config:
        orm_mode = True


# ---------- RATINGS ----------
class RatingBase(BaseModel):
    user_id: int
    movie_id: int
    rating: int


class RatingCreate(RatingBase):
    pass


class RatingResponse(RatingBase):
    rating_id: int

    class Config:
        orm_mode = True
