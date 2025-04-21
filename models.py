from database import Base
from sqlalchemy import Column, Integer, String, ForeignKey, Text, Date, Table, Float
from sqlalchemy.orm import relationship
from datetime import date



film_genre = Table('film_genre', Base.metadata, 
                   Column('id', Integer, primary_key=True, autoincrement=True, nullable=False), 
                   Column('film_id', Integer, ForeignKey('films.id'), nullable=False), 
                   Column('genre_id', Integer, ForeignKey('genres.id'), nullable=False))

class Film(Base):
    __tablename__ = 'films'
    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    name = Column(String(255), nullable=False)
    year = Column(Integer, nullable=False)
    duration = Column(Float, nullable=False)
    rating = Column(Float, nullable=True)
    desc = Column(Text, default=None, nullable=True)
    poster = Column(String(255), default=None, nullable=True)
    add_date = Column(Date, default=date.today, nullable=False)

    genres = relationship('Genre', secondary='film_genre', backref='films')

class Genre(Base):
    __tablename__ = 'genres'
    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    name = Column(String(255), unique=True, nullable=False)
    desc = Column(Text, default=None, nullable=True)

    # films = relationship('Films', secondary='film_genre', back_populates='genres')

