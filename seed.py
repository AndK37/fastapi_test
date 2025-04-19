from sqlalchemy.orm import Session
from database import engine
import models
from datetime import date
import os


models.Base.metadata.drop_all(bind=engine)
models.Base.metadata.create_all(bind=engine)

with Session(bind=engine) as session:
    os.mkdir('img')

    g1 = models.Genre(name='фантастика',
                      desc='Направление и жанр художественной кинематографии, который можно охарактеризовать повышенным уровнем условности.')

    g2 = models.Genre(name='драма',
                      desc=None)
    
    g3 = models.Genre(name='приключения',
                      desc=None)
    
    g4 = models.Genre(name='боевик',
                      desc=None)
    

    f1 = models.Film(name='Интерстеллар', 
                     year=2014, 
                     duration=169,
                     rating=8.7, 
                     poster='', 
                     genres=[g1, g2, g3])

    f2 = models.Film(name='Матрица', 
                     year=1999, 
                     duration=136,
                     rating=8.5, 
                     poster='', 
                     genres=[g1, g4])
    

    session.add(g1)
    session.add(g2)
    session.add(g3)
    session.add(g4)
    session.add(f1)
    session.add(f2)

    session.commit()