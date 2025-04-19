from database import Base
from sqlalchemy import Column, Integer, String, ForeignKey, Text, Date, Table, Float
from sqlalchemy.orm import relationship
from datetime import date



film_genre = Table('film_genre', Base.metadata, 
                   Column('id', Integer, primary_key=True, autoincrement=True), 
                   Column('film_id', Integer, ForeignKey('films.id')), 
                   Column('genre_id', Integer, ForeignKey('genres.id')))

class Film(Base):
    __tablename__ = 'films'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255))
    year = Column(Integer)
    duration = Column(Integer)
    rating = Column(Float)
    desc = Column(Text, default=None)
    poster = Column(String(255), default='')
    add_date = Column(Date, default=date.today)

    genres = relationship('Genre', secondary='film_genre', backref='films')

class Genre(Base):
    __tablename__ = 'genres'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255), unique=True)
    desc = Column(Text, default=None)

    # films = relationship('Films', secondary='film_genre', back_populates='genres')

