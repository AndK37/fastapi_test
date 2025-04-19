from fastapi import FastAPI, HTTPException, Depends
from database import get_db
from sqlalchemy.orm import Session
import models
from typing import List
import pyd



app = FastAPI()



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
def create_film(film: pyd.CreateFilm, db: Session=Depends(get_db)):
    pass

@app.put('/movies/{id}', response_model=pyd.FilmSchema)
def update_film(db: Session=Depends(get_db)):
    pass

@app.put('/movies/{id}/image', response_model=pyd.FilmSchema)
def update_film_poster(db: Session=Depends(get_db)):
    pass

@app.delete('/movies/{id}')
def delete_film(id: int, db: Session=Depends(get_db)):
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
def create_genre(genre: pyd.CreateGenre, db: Session=Depends(get_db)):
    genre_db = db.query(models.Genre).filter(models.Genre.name == genre.name).first()
    if genre_db:
        raise HTTPException(400, 'Уже существует')
    
    genre_db = models.Genre()

    genre_db.name = genre.name
    genre_db.desc = genre.desc

    db.add(genre_db)
    db.commit()

    return genre_db




