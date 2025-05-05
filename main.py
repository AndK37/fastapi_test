from fastapi import FastAPI, HTTPException, Depends, UploadFile
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from database import get_db
from sqlalchemy.orm import Session
import models
from typing import List
import pyd
from datetime import datetime
import hashlib

app = FastAPI()

security = HTTPBasic()

def verify_credentials(credentials: HTTPBasicCredentials = Depends(security), db: Session=Depends(get_db)):
    user_db =  db.query(models.User).filter(models.User.login == credentials.username).first()
    if not user_db:
        raise HTTPException(404, 'User Not Exist')
    if hash_password(credentials.password) != user_db.password:
        raise HTTPException(401, "Unvalid credentials")
    
    return credentials.username

def hash_password(password):
    h = hashlib.new('SHA256')
    h.update(password.encode())
    p_h = h.hexdigest()
    return p_h

@app.post('/users', response_model=pyd.BaseUser)
def create_user(user: pyd.CreateUser, db: Session=Depends(get_db)):
    user_db = db.query(models.User).filter(models.User.login == user.login).first()
    if user_db:
        raise HTTPException(400, "Already Exist")
    user_db = models.User()

    user_db.login = user.login
    user_db.password = hash_password(user.password)

    db.add(user_db)
    db.commit()
    
    return user_db

@app.get('/movies', response_model=List[pyd.BaseFilmShort])
def get_all_films(db: Session=Depends(get_db)):
    films = db.query(models.Film).all()

    if not films:
        raise HTTPException(404, "Не найдено")

    return films

@app.get('/movies/{id}', response_model=pyd.FilmSchema)
def get_film_by_id(id: int, db: Session=Depends(get_db)):
    film = db.query(models.Film).filter(models.Film.id == id).first()

    if not film:
        raise HTTPException(404, "Фильм не найден")

    return film

@app.post('/movies', response_model=pyd.FilmSchema)
def create_film(film: pyd.CreateFilm, db: Session=Depends(get_db), user: str = Depends(verify_credentials)):
    film_db = models.Film()
    film_db.name = film.name
    film_db.year = film.year
    film_db.duration = film.duration
    film_db.rating = film.rating
    film_db.desc = film.desc

    for genre in film.genres:
        genre_db = db.query(models.Genre).filter(models.Genre.id == genre).first()
        if genre_db:
            film_db.genres.append(genre_db)
        else:
            raise HTTPException(400, 'Неправильный жанр')

    db.add(film_db)
    db.commit()

    return film_db

@app.put('/movies/{id}', response_model=pyd.FilmSchema)
def update_film(id: int, film: pyd.CreateFilm, db: Session=Depends(get_db), user: str = Depends(verify_credentials)):
    film_db = db.query(models.Film).filter(models.Film.id == id).first()
    if not film_db:
        raise HTTPException(404, "Фильм не найден")
    
    film_db.name = film.name
    film_db.year = film.year
    film_db.duration = film.duration
    film_db.rating = film.rating
    film_db.desc = film.desc

    new_genres = []
    for genre in film.genres:
        genre_db = db.query(models.Genre).filter(models.Genre.id == genre).first()
        if genre_db:
            new_genres.append(genre_db)
        else:
            raise HTTPException(400, 'Неправильный жанр')
            
    film_db.genres = new_genres

    db.commit()

    return film_db

@app.put('/movies/{id}/image', response_model=pyd.FilmSchema)
def update_film_poster(id: int, file: UploadFile, db: Session=Depends(get_db), user: str = Depends(verify_credentials)):
    allowed_formats = ['image/png', 'image/jpeg']

    if file.content_type not in allowed_formats:
        raise HTTPException(400, 'Неправильный формат')
    
    if file.size > 2097152:
        raise HTTPException(400, 'Файл больше 2mb')
    
    file.filename = str(datetime.now().timestamp()).replace('.', '0')

    file_dir = f"./img/{file.filename}.{file.content_type[6:]}"
    with open(file_dir, "wb+") as file_object:
        file_object.write(file.file.read())

    film = db.query(models.Film).filter(models.Film.id == id).first()

    if not film:
        raise HTTPException(404, "Фильм не найден")
    
    film.poster = file_dir
    db.commit()

    return film

@app.delete('/movies/{id}')
def delete_film(id: int, db: Session=Depends(get_db), user: str = Depends(verify_credentials)):
    film = db.query(models.Film).filter(models.Film.id == id).first()
    if not film:
        raise HTTPException(404, 'Фильм не найден')
    
    db.delete(film)
    db.commit()

    return {'msg': 'Удалено'}

@app.get('/genres', response_model=List[pyd.BaseGenre])
def get_all_genres(db: Session=Depends(get_db)):
    genres = db.query(models.Genre).all()

    return genres

@app.post('/genres', response_model=pyd.BaseGenre)
def create_genre(genre: pyd.CreateGenre, db: Session=Depends(get_db), user: str = Depends(verify_credentials)):
    genre_db = db.query(models.Genre).filter(models.Genre.name == genre.name).first()
    if genre_db:
        raise HTTPException(400, 'Уже существует')
    
    genre_db = models.Genre()

    genre_db.name = genre.name
    genre_db.desc = genre.desc

    db.add(genre_db)
    db.commit()

    return genre_db

